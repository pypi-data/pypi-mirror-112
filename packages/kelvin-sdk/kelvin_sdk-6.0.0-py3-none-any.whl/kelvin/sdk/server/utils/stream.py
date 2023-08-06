from typing import Any, Callable

from starlette.responses import StreamingResponse


def build_stream_response(call: Callable, **kargs: Any) -> StreamingResponse:
    """
    Yields a stream response by building a generator with a callable that returns an OperationResponse with a stream
    attribute

    Parameters
    ----------
    call : Function that returns an OperationResponse with a stream
    kargs : Keyword arguments for the callable

    Returns
    -------
    a StreamingResponse object

    """

    def stream_generator() -> Any:
        response = call(**kargs)
        log_stream = response.stream
        if log_stream:
            for item in log_stream:
                yield item

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
