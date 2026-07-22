# from main import app
# from app.graph.workflow import run_health_workflow


# def test_health_route_exists():
#     paths = {route.path for route in app.routes if hasattr(route, "path")}
#     assert "/" in paths
#     assert "/health" in paths
#     assert "/health/database" in paths


# def test_langgraph_health_workflow():
#     assert run_health_workflow()["status"] == "ready"
