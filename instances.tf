resource "google_compute_instance_template" "vm_instance_template" {
  name         = "terraform-instance-template"
  machine_type = "e2-micro"

  disk {
    source_image = "ubuntu-os-cloud/ubuntu-minimal-2004-lts"
  }
  metadata = {
    requirements = file("./requirements.txt")
    flask = file("./server.py")
    lamport = file("./lamport.py")
    flask = file("./helloworld_pb2_grpc.py")
    flask = file("./helloworld_pb2.py")
    instance_a_address = google_compute_address.static_a.address
    instance_b_address = google_compute_address.static_b.address
    instance_c_address = google_compute_address.static_c.address
  }

  metadata_startup_script =  file("./startup.sh")

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
    }
  }
}

resource "google_compute_instance_from_template" "intance_a" {
  name = "instance-from-template-a"

  source_instance_template = google_compute_instance_template.vm_instance_template.id

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
      nat_ip = google_compute_address.static_a.address
    }
  }
}

resource "google_compute_instance_from_template" "intance_b" {
  name = "instance-from-template-b"

  source_instance_template = google_compute_instance_template.vm_instance_template.id

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
      nat_ip = google_compute_address.static_b.address
    }
  }
}

resource "google_compute_instance_from_template" "intance_c" {
  name = "instance-from-template-c"

  source_instance_template = google_compute_instance_template.vm_instance_template.id

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
      nat_ip = google_compute_address.static_c.address
    }
  }
}
