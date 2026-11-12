# 🛠️ System Maintenance and Troubleshooting Guide

## 🚀 **Quick Commands**

### **Start the System**
```bash
cd "/Users/smitapaul/Desktop/Machine Learning/poverty-resource-allocation"
./launch_system.sh
```

### **Alternative Start Method**
```bash
python3 -m streamlit run fixed_interactive_app.py --server.port 8507
```

### **Install Dependencies**
```bash
python3 -m pip install -r requirements_advanced.txt
```

## 🔧 **Troubleshooting**

### **Port Already in Use**
```bash
# Try different ports
python3 -m streamlit run fixed_interactive_app.py --server.port 8508
python3 -m streamlit run fixed_interactive_app.py --server.port 8509
```

### **Kill Existing Processes**
```bash
pkill -f "streamlit run fixed_interactive_app.py"
```

### **Check System Status**
```bash
ps aux | grep streamlit
lsof -i :8507
```

## 📊 **System Health Checks**

### **Memory Usage**
- Monitor RAM usage in Activity Monitor
- Recommended: 4GB+ available RAM
- System automatically optimizes for performance

### **Performance Metrics**
- CPU usage should stay below 80%
- Network connectivity required for real-time feeds
- Browser performance: Chrome/Safari recommended

## 🔄 **Data Backup and Recovery**

### **Manual Backup**
```bash
# Create timestamp backup
cp fixed_interactive_app.py backup/fixed_interactive_app_$(date +%Y%m%d_%H%M%S).py
cp config_advanced.json backup/config_advanced_$(date +%Y%m%d_%H%M%S).json
```

### **System Recovery**
- All session data is stored in Streamlit session state
- Data persists during browser refresh
- Full restart required only for code changes

## 🚨 **Emergency Procedures**

### **Complete System Reset**
```bash
# Stop all processes
pkill -f streamlit

# Clear cache (if needed)
streamlit cache clear

# Restart system
./launch_system.sh
```

### **Performance Issues**
1. Close unnecessary browser tabs
2. Restart the application
3. Check available system memory
4. Reduce concurrent users if needed

## 📈 **Monitoring Commands**

### **Real-time Logs**
```bash
tail -f ~/.streamlit/logs/streamlit.log
```

### **System Resources**
```bash
top -pid $(pgrep -f streamlit)
```

## 🔒 **Security Notes**

- System runs on localhost only (secure by default)
- No sensitive data is permanently stored
- Session data is isolated per user
- Automatic timeout after 1 hour of inactivity

## 📞 **Support Information**

### **System Requirements Met:**
✅ Python 3.9+  
✅ 4GB+ RAM  
✅ Modern web browser  
✅ Internet connection  

### **Critical Files:**
- `fixed_interactive_app.py` - Main application
- `config_advanced.json` - System configuration
- `requirements_advanced.txt` - Dependencies
- `launch_system.sh` - Launch script

### **Backup Files Location:**
- `./backup/` - System backups
- `./logs/` - Application logs
- Session state - In memory only
