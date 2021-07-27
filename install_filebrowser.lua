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
    os.execute('apt install -y git')
end


function install_filebrowser()
   os.execute('curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash')
end


function generate_launcher()
    os.execute('mkdir /opt/file_browser')

    destination_dir = '/opt/file_browser/start'

    launcher = io.open(destination_dir, 'w')
    launcher:write([[
#!/bin/sh
filebrowser -p 80
]])
    launcher:close()

    os.execute('chmod 755 ' .. destination_dir)
end


---------------------------------------------------------------------------------------------------


check_superuser()

install_dependencies()
install_filebrowser()
generate_launcher()

print("End of installation")
