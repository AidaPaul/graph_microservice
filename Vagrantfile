# -*- mode: ruby -*-
# vi: set ft=ruby :
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.provider "hyperv" do |v, override|
    override.vm.box = "ericmann/trusty64"
  end

  config.vm.provider "vmware_workstation" do |v, override|
    override.vm.box = "jdowning/trusty64"
  end

  config.vm.network "forwarded_port", guest: 9090, host: 9191
  config.vm.network "private_network", ip: "192.168.0.75"
  config.vm.synced_folder ".", "/opt/graph_microservice"
  config.vm.box_check_update = false
  config.vm.hostname = "graph-microservice"

  # Very crude provisioning, normally I would do it with either chef or ansible
  config.vm.provision "shell", inline: <<-SHELL
    # Bootstrap python3 env with pip and docker
    sudo apt-get update
    sudo apt-get install -y git
    sudo apt-get install -y python3-dev
    sudo apt-get install -y docker
    wget https://bootstrap.pypa.io/get-pip.py &> /dev/null
    sudo python3 get-pip.py

    # App requirements
    sudo pip3 install -r /opt/graph_microservice/requirements.txt

    # Run our docker apps
  SHELL
end