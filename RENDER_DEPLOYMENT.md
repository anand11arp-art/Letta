# Letta AI Deployment Guide for Render

## Overview
This guide provides step-by-step instructions to deploy Letta AI server to Render with Supabase PostgreSQL database.

## 🌐 Letta ADE Integration ✅

**This deployment is configured for Letta ADE (Agent Development Environment) integration!**

### **ADE Connection Details:**
- **ADE URL**: https://app.letta.com/development-servers
- **Server URL**: `https://your-app-name.onrender.com` (after deployment)
- **Password**: `kumararpit1234coc` (fixed password)
- **Secure Mode**: ✅ Enabled
- **HTTPS**: ✅ Automatic via Render

### **Quick ADE Setup:**
1. Deploy to Render (instructions below)
2. Go to https://app.letta.com/development-servers
3. Add your server with URL + password: `kumararpit1234coc`
4. Start building agents via web interface!

**See `ADE_INTEGRATION.md` for detailed ADE connection guide.**

---

The following has been automatically configured:

### Database Tables Created (40 total):
1. agent_environment_variables
2. agents  
3. agents_tags
4. alembic_version
5. archival_passages
6. archives
7. archives_agents
8. block
9. block_history
10. blocks_agents
11. file_contents
12. files
13. files_agents
14. groups
15. groups_agents
16. groups_blocks
17. identities
18. identities_agents
19. identities_blocks
20. job_messages
21. jobs
22. llm_batch_items
23. llm_batch_job
24. mcp_oauth
25. mcp_server
26. messages
27. organizations
28. prompts
29. provider_traces
30. providers
31. sandbox_configs
32. sandbox_environment_variables
33. source_passages
34. sources
35. sources_agents
36. step_metrics
37. steps
38. tools
39. tools_agents
40. users

### Migration Status:
- **Latest Alembic Version**: 5fb8bba2c373 (add_step_metrics)
- **Database**: Fully migrated and ready for production
- **Extensions**: pgvector extension configured

## 🚀 Render Deployment

### Method 1: Using render.yaml (Recommended)

1. **Fork/Clone Repository**: Upload this codebase to your GitHub repository

2. **Connect to Render**: 
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration

3. **Environment Variables**: The following are already configured in `render.yaml`:
   ```yaml
   LETTA_PG_URI: postgresql://postgres.ktmuahmsozaovcidguor:kumararpit1234coc@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require
   LETTA_PG_DB: postgres
   LETTA_PG_USER: postgres.ktmuahmsozaovcidguor
   LETTA_PG_PASSWORD: kumararpit1234coc
   LETTA_PG_HOST: aws-1-ap-southeast-1.pooler.supabase.com
   LETTA_PG_PORT: 5432
   HOST: 0.0.0.0
   PORT: 8283
   LETTA_ENVIRONMENT: PRODUCTION
   ```

### Method 2: Manual Web Service Creation

1. **Create Web Service**:
   - Go to Render Dashboard → "New" → "Web Service"
   - Connect your GitHub repository
   - Configure the following:

2. **Build & Deploy Settings**:
   - **Runtime**: Docker  
   - **Dockerfile Path**: `./Dockerfile.render`
   - **Build Command**: (Leave empty - Docker handles this)
   - **Start Command**: `python -m letta.main server --host 0.0.0.0 --port 8283`

3. **Environment Variables** (Set in Render Dashboard):
   ```
   LETTA_PG_URI=postgresql://postgres.ktmuahmsozaovcidguor:kumararpit1234coc@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require
   LETTA_ENVIRONMENT=PRODUCTION
   HOST=0.0.0.0  
   PORT=8283
   ```

## 🏥 Health Checks

The application includes:
- **Health Check Endpoint**: The server will be available at your-app.onrender.com
- **Database Connection**: Automatically verified on startup
- **Migration Check**: Runs `alembic upgrade head` on every deployment

## 🔧 Configuration Files

### Key Files Created:
- `Dockerfile.render` - Optimized Docker configuration for Render
- `render.yaml` - Render Blueprint configuration
- `start_render.sh` - Startup script with health checks
- `.env` - Environment variables (for local development)
- `setup_database.py` - Database setup and migration script

## 🚦 Deployment Status

✅ **Database Setup**: Complete  
✅ **Migration**: All 130+ migrations applied successfully  
✅ **Configuration**: Production-ready  
✅ **Docker**: Optimized Dockerfile created  
✅ **Environment**: Variables configured  

## 📊 Expected Deployment Outcome

After successful deployment, you'll have:
- **Letta AI Server**: Running on Render
- **Database**: Fully configured Supabase PostgreSQL
- **API Endpoints**: Available at `https://your-app.onrender.com`
- **Health Status**: Monitored by Render's health checks

## 🔍 Troubleshooting

### Common Issues:

1. **Database Connection**:
   - Verify Supabase connection string is correct
   - Check that pgvector extension is enabled in Supabase

2. **Build Failures**:
   - Ensure `Dockerfile.render` is in the root directory
   - Check that all dependencies are in `pyproject.toml`

3. **Runtime Issues**:
   - Check Render logs for specific error messages
   - Verify environment variables are set correctly

### Logs Access:
- Go to Render Dashboard → Your Service → "Logs" tab
- Check both build logs and runtime logs

## 🔐 Security Notes

- Database credentials are configured in environment variables
- SSL is enforced for database connections (`sslmode=require`)
- Production environment settings are enabled

## 📧 Support

For deployment issues:
1. Check Render's deployment logs
2. Verify Supabase database status  
3. Ensure all environment variables are set correctly

---

**Next Step**: Push this code to GitHub and deploy using Method 1 (render.yaml) for the smoothest deployment experience.