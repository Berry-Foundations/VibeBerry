
window.addEventListener(
	"contextmenu",
	e => {
		e.preventDefault();
	}
)

function oauth() {
	let perms = '66154304'
	let client_id = '895121185065562184'
	let url = `https://discord.com/api/oauth2/authorize?client_id=${client_id}&permissions=${perms}&scope=bot`

	window.open(url);
}

