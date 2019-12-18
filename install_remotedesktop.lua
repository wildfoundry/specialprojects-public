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
    os.execute('apt install -y tightvncserver git websockify')
end


function install_novnc_client()
    destination_dir = '/opt/remote_desktop/noVNC'
    os.execute('git clone git://github.com/kanaka/noVNC --branch=stable/v0.6 ' .. destination_dir)
end


function generate_launcher()
    destination_dir = '/opt/remote_desktop/start'

    launcher = io.open(destination_dir, 'w')
    launcher:write([[
#!/bin/sh
vncserver :1 -geometry 1920x1080 -depth 24 -dpi 96

/opt/remote_desktop/noVNC/utils/launch.sh --vnc 127.0.0.1:5901 --listen 80
]])
    launcher:close()

    os.execute('chmod 755 ' .. destination_dir)
end


---------------------------------------------------------------------------------------------------


check_superuser()

install_dependencies()
install_novnc_client()
generate_launcher()

print("")
print("To start VNC please run command: sudo /opt/remote_desktop/start")
