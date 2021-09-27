package system

main = allow

default allow = false

allow {
	input.method = "GET"
	input.path = [""]
}

allow {
	input.method = "GET"
	input.path = ["cars"]
  has_role("car_admin")
}

allow {
	input.method = "GET"
	input.path = ["cars", car_id]
  employees[input.user]
}

allow {
	input.method = "PUT"
	input.path = ["cars", car_id]
	has_role("manager")
}

allow {
	input.method = "DELETE"
	input.path = ["cars", car_id]
	has_role("manager")
}

has_role(name) {
	employee := employees[input.user]
	employee.roles[name]
}

employees = {
	"alice": {"roles": {"manager", "car_admin"}},
	"james": {"roles": {"manager"}},
	"kelly": {"roles": {"car_admin"}},
}