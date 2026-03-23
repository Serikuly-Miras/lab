#!/usr/bin/env fish

# fih

set SERVER "hz" 
set DEPLOY_BASE "/var/www/s-miras.com-releases"
set CURRENT_LINK "/var/www/s-miras.com"
set BUILD_DIR "build"
set TIMESTAMP (date +%Y%m%d_%H%M%S)
set NEW_RELEASE "$DEPLOY_BASE/$TIMESTAMP"

function stage_start
    set -g stage_start_time (date +%s)
    echo -n "$argv[1]..."
end

function stage_end
    set stage_end_time (date +%s)
    set duration (math $stage_end_time - $stage_start_time)
    if test $status -ne 0
        echo "Failed! ($(math $duration)s)"
        exit 1
    end
    echo "OK ($(math $duration)s)"
end

stage_start "Clean previous build"
rm -rf $BUILD_DIR
stage_end

stage_start "Building Evidence"
npm run build:strict > /dev/null
stage_end

stage_start "Creating release directory"
ssh $SERVER "mkdir -p $NEW_RELEASE"
stage_end

stage_start "Uploading files"
rsync -az --delete $BUILD_DIR/ $SERVER:$NEW_RELEASE/
stage_end

stage_start "Setting permissions"
ssh $SERVER "chown -R caddy:caddy $NEW_RELEASE && chmod -R 755 $NEW_RELEASE"
stage_end

stage_start "Atomic swap"
ssh $SERVER "ln -sfn $NEW_RELEASE $CURRENT_LINK"
stage_end

stage_start "Cleaning old releases (keeping last 3)"
ssh $SERVER "cd $DEPLOY_BASE && ls -t | tail -n +4 | xargs rm -rf"
stage_end

stage_start "Update Caddyfile"
ssh $SERVER "sudo cp ./Caddyfile /etc/caddy/Caddyfile"
stage_end

stage_start "Restarting Caddy"
ssh $SERVER "sudo systemctl reload caddy"
stage_end

echo "Deployment complete."