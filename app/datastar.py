from fastapi.responses import StreamingResponse


def send_event(data: str, merge=False):
    yield "event: datastar-fragment\n"
    if merge:
        yield "data: merge upsert_attributes\n"
    yield "data: fragment\n"
    for d in data.split("\n"):
        yield f"data: {d}\n"
    yield "\n"


def stream_template(frag: str) -> StreamingResponse:
    return StreamingResponse(
        send_event(frag),
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        media_type="text/event-stream",
    )
