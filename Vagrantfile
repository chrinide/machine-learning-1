## -*- mode: ruby -*-
## vi: set ft=ruby :

## All Vagrant configuration is done below. The "2" in Vagrant.configure
## configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
## you're doing.
Vagrant.configure(2) do |config|
  ## The most common configuration options are documented and commented below.
  ## For a complete reference, please see the online documentation at
  ## https://docs.vagrantup.com.

  ## Variables (ruby syntax)
  atlas_repo       = 'jeff1evesque'
  atlas_box        = 'trusty64'
  box_version      = '1.0.0'

  required_plugins = %w(vagrant-r10k vagrant-triggers vagrant-puppet-install)
  plugin_installed = false
  environment      = 'vagrant'

  ## Install Vagrant Plugins
  required_plugins.each do |plugin|
    unless Vagrant.has_plugin? plugin
      system "vagrant plugin install #{plugin}"
      plugin_installed = true
    end
  end

  ## Restart Vagrant: if new plugin installed
  if plugin_installed == true
    exec "vagrant #{ARGV.join(' ')}"
  end

  ## ensure puppet modules directory on the host before 'vagrant up'
  config.trigger.before :up do
    run "mkdir -p puppet/environment/#{environment}/modules"
    run "mkdir -p puppet/environment/#{environment}/modules_contrib"
  end

  ## Every Vagrant development environment requires a box. You can search for
  ## boxes at https://atlas.hashicorp.com/search.
  config.vm.box                        = "#{atlas_repo}/#{atlas_box}"
  config.vm.box_download_checksum      = 'c26da6ba1c169bdc6e9168125ddb0525'
  config.vm.box_url                    = "https://atlas.hashicorp.com/#{atlas_repo}/boxes/#{atlas_box}/versions/#{box_version}/providers/virtualbox.box"
  config.vm.box_download_checksum_type = 'md5'

  ## Ensure puppet installed within guest
  config.puppet_install.puppet_version = '4.9.3'

  ## Create a forwarded port mapping which allows access to a specific port
  ## within the machine from a port on the host machine. In the example below,
  ## accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network 'forwarded_port', guest: 5000, host: 8080
  config.vm.network 'forwarded_port', guest: 443, host: 8585

  ## increase RAM to ensure scrypt doesn't exhaust memory
  config.vm.provider 'virtualbox' do |v|
    v.customize ['modifyvm', :id, '--memory', '10000']
  end

  ## Run r10k
  config.r10k.puppet_dir      = "puppet/environment/#{environment}"
  config.r10k.puppetfile_path = "puppet/environment/#{environment}/Puppetfile"

  ## Custom Manifest: install needed packages
  ##
  ## Note: future parser allow array iteration in the puppet manifest
  ##
  config.vm.provision 'puppet' do |puppet|
    puppet.environment_path  = 'puppet/environment'
    puppet.environment       = environment
    puppet.manifests_path    = "puppet/environment/#{environment}/manifests"
    puppet.module_path       = [
      "puppet/environment/#{environment}/modules_contrib",
      "puppet/environment/#{environment}/modules",
    ]
    puppet.manifest_file     = 'site.pp'
    puppet.hiera_config_path = 'hiera.yaml'
  end

  ## clean up files on the host after 'vagrant destroy'
  config.trigger.after :destroy do
    run 'rm -Rf log/database'
    run 'rm -Rf log/application'
    run 'rm -Rf log/webcompiler'
    run 'rm -Rf log/webserver'
    run 'rm -Rf build'
    run 'rm -Rf interface/static/css'
    run 'rm -Rf interface/static/img'
    run 'rm -Rf interface/static/js'
    run 'rm -Rf puppet/environment/*/modules_contrib'
    run 'rm -Rf src/jsx/node_modules'
    run 'rm -f src/js/.gitignore'
    run 'rm -f src/js/content.js'
    run 'find . -name "*.pyc" -type f -exec rm -r {} +'
    run 'find . -name __pycache__ -type d -exec rm -r {} +'
    run 'find . -name .cache -type d -exec rm -r {} +'
  end
end