# CalloutRacing Project Organization Plan

## Current Issues
- Test files scattered in root directory
- SQL files mixed with Python files
- Configuration files not properly organized
- Documentation files mixed with code
- Deployment scripts scattered

## Proposed New Structure

```
CalloutRacing-1/
├── backend/                    # Django backend (existing)
│   ├── api/
│   ├── calloutracing/
│   ├── core/
│   ├── tests/
│   └── ...
├── frontend/                   # React frontend (existing)
│   ├── src/
│   ├── public/
│   └── ...
├── docs/                       # All documentation
│   ├── guides/
│   │   ├── authentication.md
│   │   ├── database-setup.md
│   │   ├── docker-setup.md
│   │   ├── environment-variables.md
│   │   ├── gmail-setup.md
│   │   ├── railway-deployment.md
│   │   ├── search-features.md
│   │   └── sso-setup.md
│   ├── stripe/
│   │   ├── direct-charges-guide.md
│   │   ├── sample-analysis.md
│   │   └── setup-guide.md
│   ├── deployment/
│   │   ├── production-readiness-checklist.md
│   │   └── secret-management-guide.md
│   └── seo/
│       └── optimization-guide.md
├── scripts/                    # All utility scripts
│   ├── database/
│   │   ├── fix_content_type_final.py
│   │   ├── fix_content_type_names.py
│   │   ├── fix_django_tables.py
│   │   ├── check_tables.py
│   │   ├── check_sqlite_tables.py
│   │   ├── check_railway_tables.py
│   │   ├── check_content_type_data.py
│   │   ├── check_content_type_structure.py
│   │   ├── connect_and_populate_railway.py
│   │   ├── migrate_db.py
│   │   ├── sync_migrations.py
│   │   └── setup_env.py
│   ├── deployment/
│   │   ├── deploy_to_production.py
│   │   └── docker-setup.bat
│   ├── testing/
│   │   ├── test_all_api_endpoints.py
│   │   ├── test_auth_endpoints.py
│   │   ├── test_auth_flow.py
│   │   ├── test_auth_working.py
│   │   ├── test_authentication_flow.py
│   │   ├── test_email_config.py
│   │   ├── test_email_verification.py
│   │   ├── test_frontend_auth.py
│   │   ├── test_port_8001.py
│   │   ├── test_social_marketplace.py
│   │   ├── comprehensive_test.py
│   │   ├── simple_test.py
│   │   └── temp_auto_verify_fix.py
│   └── database-sql/
│       ├── rebuild_database_complete.sql
│       ├── complete_schema_fix.sql
│       ├── fix_all_missing_columns.sql
│       ├── fix_core_callout_missing_columns.sql
│       ├── fix_core_user_table.sql
│       ├── fix_django_content_type.sql
│       ├── fix_production_database.sql
│       ├── cleanup_tokens.sql
│       ├── populate_sample_data.sql
│       ├── populate_sample_data_fixed.sql
│       └── real_dragstrips_population.sql
├── config/                     # Configuration files
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.prod.yml
│   │   └── Dockerfile
│   ├── nginx/
│   │   └── nginx.conf
│   ├── railway/
│   │   ├── railway.json
│   │   └── railway.toml
│   └── stripe/
│       └── stripe-sample-code.zip
├── public/                     # Static assets (existing)
├── .github/                    # GitHub workflows (existing)
├── .vscode/                    # VS Code settings (existing)
├── .gitignore
├── .dockerignore
├── package.json
├── package-lock.json
├── Procfile
├── README.md
├── robots.txt
└── sitemap.xml
```

## Migration Steps

1. Create new directory structure
2. Move files to appropriate directories
3. Update any hardcoded paths in scripts
4. Update documentation references
5. Test that everything still works

## Benefits

- Clear separation of concerns
- Easy to find specific types of files
- Better maintainability
- Professional project structure
- Easier onboarding for new developers 