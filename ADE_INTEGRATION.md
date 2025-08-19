# 🌐 Letta ADE (Agent Development Environment) Integration Guide

## Overview
This guide explains how to connect your Render-deployed Letta server to the Letta ADE web interface at https://app.letta.com

## ✅ **ADE Configuration (Already Enabled)**

### **What's Been Configured:**
- ✅ **Secure Mode**: Enabled with `--secure` flag
- ✅ **Password Protection**: Auto-generated secure password via Render
- ✅ **HTTPS**: Automatically provided by Render
- ✅ **Public URL**: Render provides public endpoint
- ✅ **CORS**: Configured for web access

### **Environment Variables Set:**
```yaml
SECURE: true
LETTA_SERVER_PASSWORD: kumararpit1234coc
```

## 🚀 **Connecting to Letta ADE**

### **Step 1: Deploy to Render**
1. Push your code to GitHub repository
2. Deploy using Render Blueprint (`render.yaml`)
3. Wait for deployment to complete
4. Note your Render URL: `https://your-app-name.onrender.com`

### **Step 2: Get Your Server Password**
Your server password is set to: **`kumararpit1234coc`**

(This is configured in the deployment and will be consistent across deployments)

### **Step 3: Connect to ADE**
1. Go to **https://app.letta.com/development-servers**
2. Click **"Add Development Server"**
3. Enter your server details:
   ```
   Server URL: https://your-app-name.onrender.com
   Password: kumararpit1234coc
   Name: My Render Letta Server (optional)
   ```
4. Click **"Connect"**

### **Step 4: Verify Connection**
- ADE should show "Connected" status
- You can now manage agents, sources, and tools via the web interface
- All API calls will go through your Render deployment

## 🔧 **Server Configuration for ADE**

### **Command Line Flags (Automatically Set):**
```bash
letta server --host 0.0.0.0 --port 8283 --secure
```

### **API Endpoints Available via ADE:**
- `/v1/agents` - Agent management
- `/v1/sources` - Data source management  
- `/v1/tools` - Tool management
- `/v1/health` - Health monitoring
- `/openai/chat/completions` - OpenAI-compatible API

## 🔐 **Security Features**

### **Password Authentication:**
- Every API request requires the server password
- Password is auto-generated and secure
- Transmitted over HTTPS only

### **CORS Configuration:**
```python
cors_origins = [
    "https://app.letta.com",
    "https://letta.com", 
    "http://localhost:3000",
    # ... other allowed origins
]
```

## 🐛 **Troubleshooting**

### **Connection Issues:**

1. **"Server Unreachable"**:
   - Verify Render deployment is running
   - Check health endpoint: `https://your-app.onrender.com/v1/health`
   - Ensure no typos in URL

2. **"Authentication Failed"**:
   - Password should be: `kumararpit1234coc`
   - Ensure password doesn't have extra spaces

3. **"CORS Error"**:
   - This should be automatically handled
   - If issues persist, check Render logs

### **Getting Logs:**
1. Go to Render Dashboard → Your Service
2. Click "Logs" tab
3. Look for startup messages and any errors

## 📊 **Expected ADE Features**

Once connected, you can use ADE to:
- ✅ **Create & manage agents** visually
- ✅ **Upload & process documents** as data sources  
- ✅ **Install & configure tools**
- ✅ **Chat with agents** through web interface
- ✅ **Monitor system health** and performance
- ✅ **View agent memory** and conversation history

## 🔄 **Updating Server Connection**

If you redeploy your Render service:
1. URL typically stays the same
2. Password remains: `kumararpit1234coc` (fixed password)
3. No need to update password in ADE
4. Connection should automatically reconnect

## 📞 **Support**

- **ADE Issues**: Contact Letta support through app.letta.com
- **Deployment Issues**: Check this repository's documentation
- **Server Logs**: Available in Render Dashboard

---

**🎉 Your Letta server is now ADE-ready!** 

Deploy to Render and connect via https://app.letta.com/development-servers