# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance
resource "google_compute_instance" "default" {
  name         = var.instance_name
  machine_type = "e2-standard-4"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 30
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata_startup_script = <<-OUTEREOF
sudo apt update
sudo apt install python3-pip -y
sudo apt install docker.io -y
sudo usermod -aG docker $USER
sudo chmod 666 /var/run/docker.sock # see https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue
pip3 install pandas==1.5.2 prefect-gcp[cloud_storage]==0.2.4 protobuf==4.21.11 pyarrow==10.0.1 pandas-gbq==0.18.1

export PREFECT_API_KEY=${var.prefect_api_key}
export DOCKERHUB_USER=${var.dockerhub_user}
export DOCKERHUB_PASSWD=${var.dockerhub_passwd}
export PREFECT_WORKSPACE=${var.prefect_workspace}

prefect cloud login -k $PREFECT_API_KEY
prefect cloud workspace set --workspace $PREFECT_WORKSPACE
echo $DOCKERHUB_PASSWD | docker login --username $DOCKERHUB_USER --password-stdin
prefect agent start -q default
OUTEREOF
}
