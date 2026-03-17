#!/usr/bin/env fish

# fih

set SERVER "hz" 
set DEPLOY_BASE "/var/www/s-miras.com-releases"
set CURRENT_LINK "/var/www/s-miras.com"
set BUILD_DIR "build"
set TIMESTAMP (date +%Y%m%d_%H%M%S)
set NEW_RELEASE "$DEPLOY_BASE/$TIMESTAMP"

echo "Building Evidence..."
npm run build:strict
if test $status -ne 0
    echo "Build failed!"
    exit 1
end

echo "Creating release directory..."
ssh $SERVER "mkdir -p $NEW_RELEASE"

echo "Uploading files..."
rsync -az --delete $BUILD_DIR/ $SERVER:$NEW_RELEASE/

echo "Setting permissions..."
ssh $SERVER "chown -R caddy:caddy $NEW_RELEASE && chmod -R 755 $NEW_RELEASE"

echo "Atomic swap..."
ssh $SERVER "ln -sfn $NEW_RELEASE $CURRENT_LINK"

echo "Cleaning old releases (keeping last 3)..."
ssh $SERVER "cd $DEPLOY_BASE && ls -t | tail -n +4 | xargs rm -rf"

echo "Deployment complete."