function getToken(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		let cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			let cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(
					cookie.substring(name.length + 1)
				);
				break;
			}
		}
	}
	return cookieValue;
}

function setCookie(name, value, days = null) {
	let expires = "";
	if (days) {
		let date = new Date();
		date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
		expires = "; expires=" + date.toUTCString();
	}
	document.cookie = name + "=" + (value || "") + expires + "; path=/";
}
function getCookie(name) {
	let nameEQ = name + "=";
	let ca = document.cookie.split(";");
	for (let i = 0; i < ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) == " ") c = c.substring(1, c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
	}
	return null;
}

// Hover effect
let hoverEffBtns = document.getElementsByClassName("hover-eff-btn");
for (let i = 0; i < hoverEffBtns.length; i++) {
	hoverEffBtns[i].addEventListener("mouseover", (e) => {
		if (e.target.tagName == "Is") {
			e.target.parentElement.classList.remove("outline");
		} else {
			e.target.classList.remove("outline");
		}
	});

	hoverEffBtns[i].addEventListener("mouseout", (e) => {
		if (e.target.tagName == "Is") {
			e.target.parentElement.classList.add("outline");
		} else {
			e.target.classList.add("outline");
		}
	});
}

// Update Item
let updateItemBtns = document.getElementsByClassName("update-item");
for (let i = 0; i < updateItemBtns.length; i++) {
	updateItemBtns[i].addEventListener("click", (e) => {
		productId = e.target.dataset.id;
		action = e.target.dataset.action;

		if (user == "AnonymousUser") {
			console.log(user);
			updateItemCookie(productId, action);
		} else {
			updateItem(productId, action);
		}
	});
}

function updateItem(productId, action) {
	url = "/update-item/";
	let csrftoken = getToken("csrftoken");

	fetch(url, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrftoken,
		},
		body: JSON.stringify({
			productId: productId,
			action: action,
		}),
	})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			location.reload();
		});
}

function updateItemCookie(productId, action) {
	order = JSON.parse(getCookie("order"));
	if (order == null) {
		order = {};
	}

	if (action == "add") {
		if (!order[productId]) {
			order[productId] = 1;
		} else {
			order[productId] += 1;
		}
	} else if (action == "remove") {
		if (!order[productId]) {
			order[productId] = 0;
		} else {
			order[productId] -= 1;
		}

		if (order[productId] < 1) {
			delete order[productId];
		}
	}

	setCookie("order", JSON.stringify(order));

	location.reload();
}
