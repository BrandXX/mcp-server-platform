# Security Guide

This document outlines security best practices for the MCP Server Development Platform.

## 🚨 **CRITICAL: API Key Security**

### **Environment Variables (Required)**

**NEVER** put API keys directly in configuration files. Always use environment variables:

```bash
# ✅ CORRECT: Use environment variables
OPENWEATHER_API_KEY=your_actual_api_key_here

# ❌ WRONG: Never put keys in config files
"env": {
  "OPENWEATHER_API_KEY": "your_api_key_here"  # This will be exposed!
}
```

### **Setup Process**

1. **Copy the template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit .env with your actual keys**:
   ```bash
   # Edit the .env file with your real API keys
   nano .env
   ```

3. **Verify .env is ignored**:
   ```bash
   git status  # .env should NOT appear in the list
   ```

## 🔒 **Environment Variable Management**

### **Required Variables**
- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key

### **Optional Variables**
- `UNITS`: Temperature units (imperial/metric)
- `DEBUG`: Enable debug logging (true/false)
- `API_TIMEOUT`: API request timeout in seconds

### **Getting API Keys**

#### OpenWeather API Key
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Generate an API key
4. Add to your `.env` file

## 🛡️ **Security Best Practices**

### **File Security**
- ✅ **Use .env files** for secrets
- ✅ **Keep .env in .gitignore**
- ✅ **Use .env.example** for templates
- ❌ **Never commit .env files**
- ❌ **Never put secrets in config files**

### **API Key Security**
- 🔄 **Rotate keys regularly**
- 📊 **Monitor API usage**
- 🚫 **Restrict key permissions**
- 🔒 **Use different keys for dev/prod**

### **Container Security**
- 🔒 **Read-only mounts** for source code
- 📁 **Writable mounts** only for data
- 🚫 **No privileged containers**
- 🔐 **Environment variable injection**

## 🚨 **If You Accidentally Expose an API Key**

### **Immediate Actions**

1. **Revoke the exposed key immediately**:
   - Go to your API provider (e.g., OpenWeatherMap)
   - Delete/revoke the exposed key

2. **Generate a new key**:
   - Create a new API key
   - Update your `.env` file

3. **Remove from Git history** (if committed):
   ```bash
   # Remove sensitive file from Git history
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch config/mcpo.json' \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push to update remote
   git push origin --force --all
   ```

4. **Update documentation**:
   - Notify users about the security incident
   - Update setup instructions

### **Prevention**
- ✅ **Always use .env files**
- ✅ **Review commits before pushing**
- ✅ **Use pre-commit hooks**
- ✅ **Regular security audits**

## 🔍 **Security Checklist**

### **Before Committing**
- [ ] No API keys in config files
- [ ] .env file is in .gitignore
- [ ] Secrets are in environment variables
- [ ] No sensitive data in logs

### **Before Deploying**
- [ ] Environment variables are set
- [ ] API keys are valid and active
- [ ] Container has minimal permissions
- [ ] Monitoring is enabled

### **Regular Maintenance**
- [ ] Rotate API keys quarterly
- [ ] Review access logs
- [ ] Update dependencies
- [ ] Security audit

## 📋 **Environment File Template**

Always use this template for new environments:

```bash
# Copy this template
cp .env.example .env

# Edit with your actual values
nano .env

# Verify it's ignored
git status  # Should not show .env
```

## 🆘 **Security Incident Response**

If you discover a security issue:

1. **Do not create a public issue**
2. **Email security concerns** to the maintainers
3. **Include details** about the vulnerability
4. **Wait for response** before public disclosure

## 🔗 **Additional Resources**

- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Environment Variable Security](https://12factor.net/config)

## 📞 **Security Contact**

For security-related issues, please contact the maintainers privately before creating public issues.

Remember: **Security is everyone's responsibility!** 🔒
