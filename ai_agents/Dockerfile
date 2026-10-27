# syntax=docker/dockerfile:1.4

FROM langchain/langgraph-api:3.11-wolfi



# -- Adding local package . --
ADD . /deps/ai_agents
# -- End of local package . --
# -- Adding local package ../packages/gestalt_models --
COPY --from=gestalt_models . /deps/packages/gestalt_models
# -- End of local package ../packages/gestalt_models --

# -- Installing all local dependencies --
# RUN for dep in /deps/*; do             echo "Installing $dep";             if [ -d "$dep" ]; then                 echo "Installing $dep";                 (cd "$dep" && PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e .);             fi;         done
RUN PYTHONDONTWRITEBYTECODE=1 pip install \
    --no-cache-dir \
    -c /api/constraints.txt \
    -e /deps/packages/gestalt_models \
    -e /deps/ai_agents
# -- End of local dependencies install --
ENV LANGSERVE_GRAPHS='{"agent": "/deps/ai_agents/src/agent/graph.py:graph"}'



# -- Ensure user deps didn't inadvertently overwrite langgraph-api
RUN mkdir -p /api/langgraph_api /api/langgraph_runtime /api/langgraph_license && touch /api/langgraph_api/__init__.py /api/langgraph_runtime/__init__.py /api/langgraph_license/__init__.py
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir --no-deps -e /api
# -- End of ensuring user deps didn't inadvertently overwrite langgraph-api --
# -- Removing build deps from the final image ~<:===~~~ --
RUN pip uninstall -y pip setuptools wheel
RUN rm -rf /usr/local/lib/python*/site-packages/pip* /usr/local/lib/python*/site-packages/setuptools* /usr/local/lib/python*/site-packages/wheel* && find /usr/local/bin -name "pip*" -delete || true
RUN rm -rf /usr/lib/python*/site-packages/pip* /usr/lib/python*/site-packages/setuptools* /usr/lib/python*/site-packages/wheel* && find /usr/bin -name "pip*" -delete || true

WORKDIR /deps/ai_agents