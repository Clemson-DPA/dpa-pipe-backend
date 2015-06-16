from rest_framework import routers

from locations import rest_api as loc_api
from products import rest_api as product_api
from ptasks import rest_api as ptask_api
from users import rest_api as user_api

api_router = routers.DefaultRouter()

# ---- locations

api_router.register(
    r'locations',
    loc_api.LocationViewSet,
)

# ---- products

api_router.register(
    r'product-categories',
    product_api.ProductCategoryViewSet,
)

api_router.register(
    r'products',
    product_api.ProductViewSet,
)

api_router.register(
    r'product-versions',
    product_api.ProductVersionViewSet,
)

api_router.register(
    r'product-representations',
    product_api.ProductRepresentationViewSet,
)

api_router.register(
    r'product-representation-statuses',
    product_api.ProductRepresentationStatusViewSet,
)

api_router.register(
    r'product-groupings',
    product_api.ProductGroupingViewSet,
)

api_router.register(
    r'product-subscriptions',
    product_api.ProductSubscriptionViewSet,
)

# ---- ptasks 

api_router.register(
    r'ptasks',
    ptask_api.PTaskViewSet,
)

api_router.register(
    r'ptask-assignments',
    ptask_api.PTaskAssignmentViewSet,
)

api_router.register(
    r'ptask-versions',
    ptask_api.PTaskVersionViewSet,
)

# ---- users

api_router.register(
    r'users',
    user_api.UserViewSet,
)

