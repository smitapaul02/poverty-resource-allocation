"""
NGO Integration and Government Notification System
Includes real-time notifications, proximity matching, and resource coordination
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from geopy.distance import geodesic
import phonenumbers
from phonenumbers import carrier, geocoder
from dataclasses import dataclass
from pydantic import BaseModel, EmailStr, validator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PovertyAlert:
    """Data class for poverty alerts"""
    district_id: str
    district_name: str
    state: str
    poverty_level: str
    coordinates: Tuple[float, float]
    population_affected: int
    resources_needed: List[str]
    urgency_score: float
    alert_time: datetime
    description: str

class NGOContact(BaseModel):
    """Pydantic model for NGO contact validation"""
    ngo_id: str
    name: str
    email: EmailStr
    phone: str
    whatsapp: Optional[str] = None
    
    @validator('phone')
    def validate_phone(cls, v):
        try:
            parsed = phonenumbers.parse(v, "IN")
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Invalid phone number")
            return v
        except:
            raise ValueError("Invalid phone number format")

class NGOMatchingEngine:
    """Engine for matching poverty areas with appropriate NGOs"""
    
    def __init__(self, ngo_database_path: str = 'data/ngo_database.json'):
        self.ngo_database_path = ngo_database_path
        self.ngos = self._load_ngo_database()
        self.government_contacts = self._load_government_contacts()
        
    def _load_ngo_database(self) -> List[Dict]:
        """Load NGO database from JSON file"""
        try:
            with open(self.ngo_database_path, 'r') as f:
                data = json.load(f)
                return data.get('ngos', [])
        except FileNotFoundError:
            logger.error(f"NGO database not found at {self.ngo_database_path}")
            return []
    
    def _load_government_contacts(self) -> List[Dict]:
        """Load government department contacts"""
        try:
            with open(self.ngo_database_path, 'r') as f:
                data = json.load(f)
                return data.get('government_departments', [])
        except FileNotFoundError:
            return []
    
    def find_nearby_ngos(self, alert: PovertyAlert, max_distance_km: float = 100) -> List[Dict]:
        """Find NGOs within specified distance of poverty-stricken area"""
        
        nearby_ngos = []
        alert_coords = alert.coordinates
        
        for ngo in self.ngos:
            ngo_coords = tuple(ngo['location']['coordinates'])
            distance = geodesic(alert_coords, ngo_coords).kilometers
            
            if distance <= max_distance_km:
                # Calculate relevance score
                relevance_score = self._calculate_ngo_relevance(ngo, alert, distance)
                
                ngo_info = ngo.copy()
                ngo_info['distance_km'] = distance
                ngo_info['relevance_score'] = relevance_score
                
                nearby_ngos.append(ngo_info)
        
        # Sort by relevance score (descending)
        nearby_ngos.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return nearby_ngos
    
    def _calculate_ngo_relevance(self, ngo: Dict, alert: PovertyAlert, distance: float) -> float:
        """Calculate relevance score for NGO based on specialization and proximity"""
        
        # Base score from distance (closer = higher score)
        distance_score = max(0, 1 - (distance / 100))  # Normalize to 0-1
        
        # Specialization match score
        ngo_specializations = set(ngo.get('specialization', []))
        required_resources = set(alert.resources_needed)
        
        # Map resources to specializations
        resource_mapping = {
            'food': {'food', 'nutrition', 'child_welfare'},
            'healthcare': {'healthcare', 'medical', 'elderly_care'},
            'education': {'education', 'literacy', 'skill_development'},
            'infrastructure': {'rural_development', 'infrastructure'},
            'water': {'clean_water', 'sanitation', 'hygiene'}
        }
        
        specialization_match = 0
        for resource in required_resources:
            mapped_specs = resource_mapping.get(resource, {resource})
            if ngo_specializations.intersection(mapped_specs):
                specialization_match += 1
        
        specialization_score = min(1.0, specialization_match / len(required_resources))
        
        # Capacity score
        capacity_score = min(1.0, ngo.get('capacity', {}).get('beneficiaries', 1000) / 10000)
        
        # Rating score
        rating_score = ngo.get('rating', 3.0) / 5.0
        
        # Response time score (faster = better)
        response_time = ngo.get('response_time_hours', 24)
        response_score = max(0, 1 - (response_time / 48))
        
        # Combined relevance score
        relevance_score = (
            distance_score * 0.3 +
            specialization_score * 0.35 +
            capacity_score * 0.15 +
            rating_score * 0.1 +
            response_score * 0.1
        )
        
        return relevance_score
    
    def get_government_contacts(self, alert: PovertyAlert) -> List[Dict]:
        """Get relevant government department contacts"""
        
        relevant_depts = []
        
        for dept in self.government_contacts:
            dept_specializations = set(dept.get('specialization', []))
            required_resources = set(alert.resources_needed)
            
            # Check if department can handle any of the required resources
            if dept_specializations.intersection(required_resources):
                relevant_depts.append(dept)
        
        return relevant_depts

class NotificationSystem:
    """System for sending notifications to NGOs and government departments"""
    
    def __init__(self, email_config: Dict = None):
        self.email_config = email_config or {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'poverty.allocation.system@gmail.com',
            'sender_password': 'your_app_password'  # Use app password for Gmail
        }
    
    def send_alert_notification(self, alert: PovertyAlert, recipients: List[Dict], 
                               notification_type: str = 'ngo') -> Dict[str, bool]:
        """Send alert notifications to recipients"""
        
        results = {}
        
        for recipient in recipients:
            try:
                # Send email notification
                email_sent = self._send_email_notification(alert, recipient, notification_type)
                
                # Send SMS notification (if enabled)
                sms_sent = self._send_sms_notification(alert, recipient)
                
                # Send WhatsApp notification (if enabled)
                whatsapp_sent = self._send_whatsapp_notification(alert, recipient)
                
                results[recipient.get('id', recipient.get('name', 'Unknown'))] = {
                    'email': email_sent,
                    'sms': sms_sent,
                    'whatsapp': whatsapp_sent
                }
                
            except Exception as e:
                logger.error(f"Failed to send notification to {recipient.get('name', 'Unknown')}: {str(e)}")
                results[recipient.get('id', recipient.get('name', 'Unknown'))] = {
                    'email': False,
                    'sms': False,
                    'whatsapp': False,
                    'error': str(e)
                }
        
        return results
    
    def _send_email_notification(self, alert: PovertyAlert, recipient: Dict, 
                                notification_type: str) -> bool:
        """Send email notification"""
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = recipient['contact']['email']
            
            if notification_type == 'ngo':
                msg['Subject'] = f"🚨 Urgent: Poverty Alert in {alert.district_name}, {alert.state}"
                body = self._create_ngo_email_body(alert, recipient)
            else:
                msg['Subject'] = f"📊 Government Alert: Poverty Situation in {alert.district_name}"
                body = self._create_government_email_body(alert, recipient)
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['sender_password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {recipient['name']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient.get('name', 'Unknown')}: {str(e)}")
            return False
    
    def _create_ngo_email_body(self, alert: PovertyAlert, ngo: Dict) -> str:
        """Create HTML email body for NGO notification"""
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <header style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; text-align: center;">🚨 URGENT POVERTY ALERT</h1>
                    <p style="margin: 10px 0 0 0; text-align: center; font-size: 18px;">Immediate Assistance Required</p>
                </header>
                
                <div style="background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px;">
                    <h2 style="color: #d73027; margin-top: 0;">📍 Location Details</h2>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>District:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert.district_name}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>State:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert.state}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Poverty Level:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;"><span style="background: #d73027; color: white; padding: 2px 8px; border-radius: 4px;">{alert.poverty_level}</span></td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Population Affected:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert.population_affected:,}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Distance from your location:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{ngo.get('distance_km', 0):.1f} km</td></tr>
                    </table>
                    
                    <h2 style="color: #d73027; margin-top: 20px;">🆘 Resources Urgently Needed</h2>
                    <ul style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #d73027;">
                        {''.join([f'<li style="margin: 5px 0; font-weight: bold; color: #d73027;">🔸 {resource.replace("_", " ").title()}</li>' for resource in alert.resources_needed])}
                    </ul>
                    
                    <h2 style="color: #d73027;">📝 Situation Description</h2>
                    <p style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #d73027;">{alert.description}</p>
                    
                    <h2 style="color: #d73027;">⚡ Urgency Score</h2>
                    <div style="background: white; padding: 15px; border-radius: 5px; text-align: center;">
                        <span style="font-size: 24px; font-weight: bold; color: #d73027;">{alert.urgency_score:.1f}/10</span>
                        <p style="margin: 5px 0 0 0; color: #666;">Higher score indicates more urgent need</p>
                    </div>
                    
                    <h2 style="color: #1a759f;">🤝 Why We're Contacting You</h2>
                    <div style="background: #e1f5fe; padding: 15px; border-radius: 5px; border-left: 4px solid #1a759f;">
                        <p><strong>Your Specialization Match:</strong> {', '.join(ngo.get('specialization', []))}</p>
                        <p><strong>Your Capacity:</strong> {ngo.get('capacity', {}).get('beneficiaries', 'N/A'):,} beneficiaries</p>
                        <p><strong>Relevance Score:</strong> {ngo.get('relevance_score', 0):.2f}/1.0</p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <p style="font-size: 18px; color: #d73027; font-weight: bold;">🔥 IMMEDIATE ACTION REQUIRED 🔥</p>
                        <p>Lives depend on quick response. Please contact us immediately if you can assist.</p>
                    </div>
                    
                    <footer style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                        <p style="color: #666;">📞 Emergency Contact: +91-11-12345678</p>
                        <p style="color: #666;">📧 poverty.allocation.system@gmail.com</p>
                        <p style="color: #666; font-size: 12px;">Sent by AI-Powered Poverty Allocation System | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </footer>
                </div>
            </div>
        </body>
        </html>
        """
        return html_body
    
    def _create_government_email_body(self, alert: PovertyAlert, dept: Dict) -> str:
        """Create HTML email body for government notification"""
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h1>Government Poverty Alert</h1>
            <h2>Location: {alert.district_name}, {alert.state}</h2>
            <p><strong>Poverty Level:</strong> {alert.poverty_level}</p>
            <p><strong>Population Affected:</strong> {alert.population_affected:,}</p>
            <p><strong>Urgency Score:</strong> {alert.urgency_score:.1f}/10</p>
            <p><strong>Resources Needed:</strong> {', '.join(alert.resources_needed)}</p>
            <p><strong>Description:</strong> {alert.description}</p>
            <p><strong>Department Programs:</strong> {', '.join(dept.get('programs', []))}</p>
            <p>Generated by AI Poverty Allocation System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
        </html>
        """
        return html_body
    
    def _send_sms_notification(self, alert: PovertyAlert, recipient: Dict) -> bool:
        """Send SMS notification (placeholder - requires SMS service integration)"""
        
        try:
            phone = recipient['contact']['phone']
            message = f"POVERTY ALERT: {alert.district_name}, {alert.state} - Level: {alert.poverty_level} - Urgency: {alert.urgency_score:.1f}/10 - Contact: poverty.allocation.system@gmail.com"
            
            logger.info(f"SMS sent to {phone}: {message[:100]}...")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            return False
    
    def _send_whatsapp_notification(self, alert: PovertyAlert, recipient: Dict) -> bool:
        """Send WhatsApp notification (placeholder - requires WhatsApp Business API)"""
        
        try:
            whatsapp = recipient['contact'].get('whatsapp')
            if not whatsapp:
                return False
            
            message = f"POVERTY ALERT: {alert.district_name}, {alert.state} - Level: {alert.poverty_level} - Urgency: {alert.urgency_score:.1f}/10 - Resources: {', '.join(alert.resources_needed)} - Contact: poverty.allocation.system@gmail.com"
            
            logger.info(f"WhatsApp message sent to {whatsapp}: {message[:100]}...")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {str(e)}")
            return False

class RealTimeAlertSystem:
    """Real-time poverty alert and coordination system"""
    
    def __init__(self, config_path: str = 'config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.ngo_engine = NGOMatchingEngine()
        self.notification_system = NotificationSystem()
        self.active_alerts = []
        
    def create_poverty_alert(self, district_data: Dict, urgency_multiplier: float = 1.0) -> PovertyAlert:
        """Create a poverty alert from district data"""
        
        # Calculate urgency score
        urgency_score = self._calculate_urgency_score(district_data) * urgency_multiplier
        
        # Determine resources needed based on poverty indicators
        resources_needed = self._determine_required_resources(district_data)
        
        # Generate description
        description = self._generate_alert_description(district_data, urgency_score)
        
        alert = PovertyAlert(
            district_id=district_data.get('District_ID', f"DIST_{datetime.now().strftime('%Y%m%d%H%M%S')}"),
            district_name=district_data['District'],
            state=district_data.get('State', 'Unknown'),
            poverty_level=district_data.get('Poverty_Level', 'Unknown'),
            coordinates=(
                district_data.get('Latitude', 20.5937),
                district_data.get('Longitude', 78.9629)
            ),
            population_affected=district_data.get('Population', 100000),
            resources_needed=resources_needed,
            urgency_score=urgency_score,
            alert_time=datetime.now(),
            description=description
        )
        
        return alert
    
    def _calculate_urgency_score(self, district_data: Dict) -> float:
        """Calculate urgency score based on multiple factors"""
        
        score = 0.0
        
        # Poverty level scoring
        poverty_level = district_data.get('Poverty_Level', 'Medium')
        if poverty_level == 'Critical':
            score += 4.0
        elif poverty_level == 'High':
            score += 3.0
        elif poverty_level == 'Medium':
            score += 2.0
        else:
            score += 1.0
        
        # Infrastructure scoring (lower = more urgent)
        infra_score = district_data.get('Infrastructure_Score', 50)
        score += (100 - infra_score) / 25  # Max 4 points
        
        # Healthcare access (lower = more urgent)
        healthcare = district_data.get('Healthcare_Index', 50)
        score += (100 - healthcare) / 50  # Max 2 points
        
        # Ensure score is between 0-10
        return min(10.0, max(0.0, score))
    
    def _determine_required_resources(self, district_data: Dict) -> List[str]:
        """Determine required resources based on district indicators"""
        
        resources = []
        
        # Food security
        if district_data.get('Employment_Rate', 50) < 40:
            resources.append('food')
        
        # Healthcare
        if district_data.get('Healthcare_Index', 50) < 50:
            resources.append('healthcare')
        
        # Education
        if district_data.get('Literacy_Rate', 70) < 60:
            resources.append('education')
        
        # Infrastructure
        if district_data.get('Infrastructure_Score', 50) < 50:
            resources.append('infrastructure')
        
        # Water and sanitation
        if district_data.get('Clean_Water_Access', 80) < 70:
            resources.append('water')
        
        return resources if resources else ['general_assistance']
    
    def _generate_alert_description(self, district_data: Dict, urgency_score: float) -> str:
        """Generate detailed alert description"""
        
        description = f"""Poverty assessment for {district_data['District']} indicates {district_data.get('Poverty_Level', 'significant')} poverty levels affecting approximately {district_data.get('Population', 100000):,} people.

Key Indicators:
- Literacy Rate: {district_data.get('Literacy_Rate', 'N/A')}%
- Employment Rate: {district_data.get('Employment_Rate', 'N/A')}%  
- Healthcare Index: {district_data.get('Healthcare_Index', 'N/A')}
- Infrastructure Score: {district_data.get('Infrastructure_Score', 'N/A')}
- Clean Water Access: {district_data.get('Clean_Water_Access', 'N/A')}%

This area requires immediate attention and coordinated relief efforts. The urgency score of {urgency_score:.1f}/10 indicates {'critical' if urgency_score >= 7 else 'high' if urgency_score >= 5 else 'moderate'} priority for intervention."""
        
        return description.strip()
    
    def process_poverty_alert(self, alert: PovertyAlert, max_distance_km: float = 100) -> Dict:
        """Process a poverty alert and notify relevant organizations"""
        
        logger.info(f"Processing poverty alert for {alert.district_name}, {alert.state}")
        
        # Find nearby NGOs
        nearby_ngos = self.ngo_engine.find_nearby_ngos(alert, max_distance_km)
        
        # Get government contacts
        government_contacts = self.ngo_engine.get_government_contacts(alert)
        
        # Send notifications
        ngo_notifications = {}
        govt_notifications = {}
        
        if nearby_ngos:
            logger.info(f"Found {len(nearby_ngos)} nearby NGOs")
            ngo_notifications = self.notification_system.send_alert_notification(
                alert, nearby_ngos[:5], 'ngo'  # Send to top 5 NGOs
            )
        
        if government_contacts:
            logger.info(f"Notifying {len(government_contacts)} government departments")
            govt_notifications = self.notification_system.send_alert_notification(
                alert, government_contacts, 'government'
            )
        
        # Store alert
        self.active_alerts.append({
            'alert': alert,
            'nearby_ngos': nearby_ngos,
            'government_contacts': government_contacts,
            'ngo_notifications': ngo_notifications,
            'govt_notifications': govt_notifications,
            'processed_at': datetime.now()
        })
        
        result = {
            'alert_id': alert.district_id,
            'status': 'processed',
            'ngos_contacted': len(ngo_notifications),
            'govt_depts_contacted': len(govt_notifications),
            'nearby_ngos': len(nearby_ngos),
            'notification_results': {
                'ngos': ngo_notifications,
                'government': govt_notifications
            }
        }
        
        logger.info(f"Alert processed successfully: {result}")
        return result
    
    def get_alert_status(self, alert_id: str) -> Optional[Dict]:
        """Get status of a specific alert"""
        
        for alert_data in self.active_alerts:
            if alert_data['alert'].district_id == alert_id:
                return {
                    'alert_id': alert_id,
                    'district': alert_data['alert'].district_name,
                    'state': alert_data['alert'].state,
                    'urgency_score': alert_data['alert'].urgency_score,
                    'resources_needed': alert_data['alert'].resources_needed,
                    'ngos_contacted': len(alert_data['ngo_notifications']),
                    'govt_contacted': len(alert_data['govt_notifications']),
                    'processed_at': alert_data['processed_at'].isoformat()
                }
        
        return None
    
    def get_active_alerts_summary(self) -> Dict:
        """Get summary of all active alerts"""
        
        if not self.active_alerts:
            return {'total_alerts': 0, 'alerts': []}
        
        summary = {
            'total_alerts': len(self.active_alerts),
            'alerts': []
        }
        
        for alert_data in self.active_alerts:
            alert = alert_data['alert']
            summary['alerts'].append({
                'alert_id': alert.district_id,
                'district': alert.district_name,
                'state': alert.state,
                'poverty_level': alert.poverty_level,
                'urgency_score': alert.urgency_score,
                'population_affected': alert.population_affected,
                'alert_time': alert.alert_time.isoformat(),
                'status': 'active'
            })
        
        return summary

def demo_alert_system():
    """Demonstrate the alert system with sample data"""
    
    # Sample district data
    sample_district = {
        'District': 'Demonstration District',
        'State': 'Sample State',
        'Poverty_Level': 'High',
        'Literacy_Rate': 35.5,
        'Employment_Rate': 25.8,
        'Healthcare_Index': 28.3,
        'Infrastructure_Score': 22.1,
        'Clean_Water_Access': 45.2,
        'Population': 150000,
        'Latitude': 20.5937,
        'Longitude': 78.9629
    }
    
    # Initialize alert system
    alert_system = RealTimeAlertSystem()
    
    # Create and process alert
    alert = alert_system.create_poverty_alert(sample_district)
    result = alert_system.process_poverty_alert(alert)
    
    print("🚨 DEMO: Poverty Alert System")
    print("=" * 50)
    print(f"Alert ID: {result['alert_id']}")
    print(f"NGOs Contacted: {result['ngos_contacted']}")
    print(f"Government Departments Contacted: {result['govt_depts_contacted']}")
    print(f"Nearby NGOs Found: {result['nearby_ngos']}")
    print("=" * 50)
    
    return result

if __name__ == "__main__":
    demo_alert_system()
