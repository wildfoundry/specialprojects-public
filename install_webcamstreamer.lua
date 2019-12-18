#!/usr/bin/env lua


function check_superuser()
    tmp = assert(io.popen('id -u', 'r')) 
    current_user = assert(tmp:read('*a'))
    tmp:close()
    current_user = string.gsub(current_user, "\n", "")
    root_user = '0'

    if current_user ~= root_user then 
        print('Please execute this script as root user.') 
        os.exit()
    end
end


function install_dependencies()
    os.execute('apt install -y build-essential debhelper libv4l-dev libjpeg8-dev libssl-dev git')
end


function install_hawkeye()
    destination_dir = '/opt/webcam_streamer/hawkeye'

    os.execute('git clone git://github.com/ipartola/hawkeye.git ' .. destination_dir)
    os.execute('make --directory ' .. destination_dir)
    os.execute('make install --directory ' .. destination_dir)
end


function generate_hawkeye_config()
    destination_dir = '/opt/webcam_streamer/conf'

    conf = io.open(destination_dir, 'w')
    conf:write([[
# IPv4 and IPv6 addresses and hostnames are supported.
host = localhost  # Secure default. If you want to listen on all interfaces try ::0 or 0.0.0.0
port = 80

# Optional. Where the static files are located.
www-root = /opt/webcam_streamer/hawkeye/www

# Optional. You can password-protect your video streams
# DANGER: unless you are also using cert and key options to wrap the video
# streams in SSL, these will be visible to everyone and provide NO SECURITY.

#auth = user:pass

# Optional. If you are planning on viewing the video streams over an
# untrusted network such as the Internet, you should use HTTPS. Obtain
# an SSL certificate/private key and specify its location below.
# NOTE: this is pretty much required for the auth option, as without it
# any motivated person can see your stream and username/password

#cert = /etc/hawkeye/hawkeye.crt
#key = /etc/hawkeye/hawkeye.key

fps = 15
width = 640
height = 480
# Only has an effect if format is set to yuv
quality = 80

log = /var/log/hawkeye.log
pid = /var/run/hawkeye/hawkeye.pid

# This is a : separated list of devices. For example:
# devices /dev/video0:/dev/video1
devices = /dev/video0

# alternative: yuv
format = mjpeg

# Comment out to run as root
#user = hawkeye
#group = hawkeye

# Options are debug, info, warning, error
log-level = info
]])
    conf:close()

    os.execute('chmod 644 ' .. destination_dir)
end


function generate_launcher()
    destination_dir = '/opt/webcam_streamer/start'

    launcher = io.open(destination_dir, 'w')
    launcher:write([[
#!/bin/sh
hawkeye -c /opt/webcam_streamer/conf
]])
    launcher:close()

    os.execute('chmod 755 ' .. destination_dir)
end


---------------------------------------------------------------------------------------------------


check_superuser()

install_dependencies()
install_hawkeye()
generate_hawkeye_config()
generate_launcher()


print("")
print("Hawekeye installed.")
print("To start streaming please run command: sudo /opt/webcam_streamer/start")
print("Then go to your wormhole address.")