base_dir = File.expand_path File.dirname(__FILE__)

Vagrant.configure("2") do |config|

    config.vm.define "day_score main", primary: true do |day_score|
        # Base box
        day_score.vm.box = "ubuntu/bionic64"
        # VM properties
        day_score.vm.provider "virtualbox" do |v|
            v.name = "day_score main development VM"
            v.customize ["modifyvm", :id, "--memory", "2048"]
            v.cpus = 2
        end
        # Port forwarding

            # Nginx reverse proxy
            day_score.vm.network :forwarded_port, guest: 80, host: 8080, auto_correct: true

            # WebPack
            day_score.vm.network :forwarded_port, guest: 8000, host: 8000, auto_correct: true
            day_score.vm.network :forwarded_port, guest: 8001, host: 8001, auto_correct: true
            day_score.vm.network :forwarded_port, guest: 8079, host: 8079, auto_correct: true

        # Folder sharing
        day_score.vm.synced_folder "#{base_dir}/", "/webapps/day_score", create: true, group: "vagrant", owner: "vagrant"

      
    end    

    # Run Ansible from the Vagrant VM
    config.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "/webapps/day_score/ansible/plays/start.yml"
        ansible.extra_vars = {"target" => "127.0.0.1",}
        ansible.inventory_path = "ansible/hosts"
        ansible.limit = "local"
    end
end
