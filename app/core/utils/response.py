from app.core.schemas.response import ResponseEnvelope


def success_response(data, meta=None):
    return ResponseEnvelope(
        success=True,
        data=data,
        error=None,
        meta=meta
    )
