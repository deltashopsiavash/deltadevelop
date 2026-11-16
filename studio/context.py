from .models import StudioProfile


def studio_context(request):
    try:
        profile = StudioProfile.load()
    except Exception:
        # Database might not yet be migrated; health-check and installation
        # should still report their own errors without leaking tracebacks.
        profile = None
    return {"studio_profile": profile}
