# Validates base_dir as a valid symlink pointing to our env and returns fully qualifed path to root
# Params:
# +base_link+:: +String+ path to base symlink
def env_root (base_link)
  # assert base_dir points to a valid symlink
  if not File.symlink?(base_link)
    throw 'Error: please create a /server link pointing to the environment root'
  end

  # assert base_dir points to our environment root
  if %-#{File.readlink(base_link)}/#{File.basename(VAGRANT_FILE)}- != VAGRANT_FILE
    throw "Error: #{base_link} link does not point at this environment root (did you link with a trailing slash?)"
  end

  return File.readlink(base_link)
end

def auto_config_host ()
  changes = false
  
  # place flag on host machine for use in common shell scripts
  if not File.exist?('/etc/.vagranthost')
    puts '==> host: Touching host indicator'
    system %-sudo touch /etc/.vagranthost-
    changes = true
  end

  # create symlink to profile.d scripts
  if not File.symlink?('/etc/profile.d')
    puts "==> host: Linking /etc/profile.d -> #{VAGRANT_DIR}/etc/profile.d"
    system %-sudo ln \-s #{VAGRANT_DIR}/etc/profile.d /etc/profile.d-
    changes = true
  end

  # enable profile.d scripts on host
  if not %x{grep '## VAGRANT START ##' /etc/profile}.strip!
    puts "==> host: Configuring /etc/profile for running sub-scripts"

    profile_script=%-
for i in /etc/profile.d/*.sh ; do
    if [ \-r "$i" ]; then
        if [ "${\-#*i}" != "$\-" ]; then
            . "$i"
        else
            . "$i" >/dev/null 2>&1
        fi
    fi
done
unset i
-

    # append script to /etc/profile and then execute that new portion to pickup env configuration
    system %-
      printf "\n## VAGRANT START ##%s## VAGRANT END ##\n" '#{profile_script}'| sudo tee \-a /etc/profile > /dev/null
    -
    changes = true
  end
  
  if changes
    puts '==> host: Auto configuration complete'
    puts 'Please re-run the command in a new shell...'
    exit 1
  end
  
  if changes == false && ENV['VAGRANT_ENV_ARE_SET'] != '1'
    puts 'Please re-run the command in a new shell...'
    exit 1
  end
end
