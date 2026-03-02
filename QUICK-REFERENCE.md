# MkDocs PoC - Quick Reference Card

**Ready to run**: `run_mkdocs_poc.bat`

---

## Commands

```batch
REM Zero-setup execution (recommended)
run_mkdocs_poc.bat

REM Full build (generate + build + validate)
python scripts\build_mkdocs.py --all

REM Generate site structure only
python scripts\build_mkdocs.py --generate

REM Build static HTML only
python scripts\build_mkdocs.py --build

REM Clean rebuild
python scripts\build_mkdocs.py --clean --all
```

---

## Generated Artifacts

| Location | Contents |
|----------|----------|
| `mkdocs-sample/docs/` | Markdown source files |
| `mkdocs-sample/site/` | Static HTML (deploy this) |
| `debug/` | Debug artifacts |
| `evidence/test-results/` | Test evidence |
| `logs/` | Execution logs |
| `output/test-reports/` | Validation reports |

---

## Testing Workflow

1. **Generate site**: Run `run_mkdocs_poc.bat`
2. **Test SharePoint**: Upload `mkdocs-sample/site/` to SPO
3. **Test Azure**: Deploy `mkdocs-sample/site/` to Azure Static Website
4. **Validate**: Use `VALIDATION-CHECKLIST.md`
5. **Report**: Document findings in `evidence/test-results/`

---

## Key Files

- `README.md` - Project overview
- `VALIDATION-CHECKLIST.md` - Test procedures
- `IMPLEMENTATION-COMPLETE.md` - Build details
- `.github/copilot-instructions.md` - AI assistant config

---

## Success Indicators

- ✅ All output uses ASCII characters ([PASS], [FAIL], [INFO])
- ✅ Site builds without errors
- ✅ All content files generated
- ✅ Debug artifacts captured
- ✅ Ready for hosting tests

---

**Status**: ✅ Implementation Complete - Ready to Execute
