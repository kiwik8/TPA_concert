docker buildx build \
--platform linux/arm64,linux/arm/v7 \
-t martingouv/concert:nginx ./nginx/ --push