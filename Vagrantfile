# -*- mode: ruby -*-
# vi: set ft=ruby :

ipythonPort = 8001                 # Ipython port to forward (also set in IPython notebook config)

$script = <<-SCRIPT

# create alias for file sync
echo "alias sync='rm -rf /home/vagrant/* && ln -s /vagrant/* /home/vagrant/.'" >> /home/vagrant/.bashrc
echo "alias free='lsof -t -i :8001 | xargs kill'" >> /home/vagrant/.bashrc

# install java8 scala git
sudo add-apt-repository ppa:openjdk-r/ppa
sudo apt-get update
sudo apt-get install -y openjdk-8-jdk scala git

# install spark 2.3 and remove spark 1.3
curl http://apache.cs.utah.edu/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz | sudo tar xvz -C /usr/local/bin
sudo rm -rf /usr/local/bin/spark-1.3.1-bin-hadoop2.6/

# update env variables
echo "export SPARK_HOME=/usr/local/bin/spark-2.3.0-bin-hadoop2.7" >> /home/vagrant/.bashrc
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-i386/jre" >> /home/vagrant/.bashrc
echo "export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/bin/spark-2.3.0-bin-hadoop2.7/bin" >> /home/vagrant/.bashrc

# use java8
sudo update-alternatives --set java /usr/lib/jvm/java-8-openjdk-i386/jre/bin/java

# update python path
echo "export PYTHONPATH=/usr/local/games:/usr/local/bin/spark-2.3.0-bin-hadoop2.7/python:/usr/local/games:/usr/local/bin/spark-2.3.0-bin-hadoop2.7/python/lib/py4j-0.10.6-src.zip:$PYTHONPATH" >> /home/vagrant/.bashrc

SCRIPT

Vagrant.configure(2) do |config|
  config.ssh.insert_key = true
  config.vm.synced_folder "./vagrant", "/vagrant", type: "virtualbox"
  config.vm.define "sparkvm2" do |master|
    master.vm.box = "sparkmooc/base2"
    master.vm.box_download_insecure = true
    master.vm.boot_timeout = 900
    master.vm.network :forwarded_port, host: ipythonPort, guest: ipythonPort, auto_correct: true   # IPython port (set in notebook config)
    master.vm.network :forwarded_port, host: 4040, guest: 4040, auto_correct: true                 # Spark UI (Driver)
    master.vm.hostname = "sparkvm2"
    master.vm.usable_port_range = 4040..4090

    master.vm.provider "virtualbox" do |vb|
      vb.name = master.vm.hostname.to_s
      vb.memory = "2600"
    end
    config.vm.provision "shell", inline: $script
  end
end