# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'optparse'

Vagrant::Config.run do |config|
  #
  # Set VirtualBox-specific options
  #
  #config.vm.customize ["modifyvm", :id, "--name", "dpa_server"]
  # TODO: Figure out how to do `gui = True`

  #
  # Hack to get Vagrant to use Vagrant Cloud images.
  #
  config.vm.box = "trusty64"
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

  config.vm.provision :shell, :path => "provision/bootstrap.sh"
  config.vm.provision :puppet, :manifests_path => "provision/manifests"

  # port forwarding 
  config.vm.forward_port 8000, 8000
  config.vm.forward_port 80, 8080
end
