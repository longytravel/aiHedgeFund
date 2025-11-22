# Security Architecture

**MVP Security (Phase 1):**
- ✅ Environment variable-based secrets (`.env` file, never committed)
- ✅ HTTPS in production (Cloudflare/nginx reverse proxy)
- ✅ CORS configuration (restrict frontend origin)
- ✅ Input validation (Pydantic schemas on all API endpoints)
- ❌ Authentication: None (single-user local deployment)
- ❌ Rate limiting: None (trusted local environment)

**Phase 2 Security (Multi-User):**
- JWT token-based authentication
- Role-based access control (admin, trader, viewer)
- API rate limiting (per-user quotas)
- Audit logging for all trades and config changes
- Encrypted database fields (API keys, trade credentials)

**Data Protection:**
- Database backups (daily automated exports)
- API key rotation (manual for MVP, automated in Phase 2)
- No sensitive data in logs (mask API keys, trade amounts)

---
