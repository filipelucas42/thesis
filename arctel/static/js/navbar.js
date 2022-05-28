const hamburger = document.getElementById('hamburger');
const hamburgerClass = document.querySelector('.hamburger');
const navbar = document.getElementById('navbar-ul');
const navDropdown = document.querySelectorAll('.navbar-ul-drop');
const drops = document.querySelectorAll('.dropdown-menu-items');

hamburger.addEventListener('click', () => {
  navbar.classList.toggle('collapse-nav');
  hamburgerClass.classList.toggle('nav-open');
})

navDropdown.forEach(btn => {
  btn.onclick = () => {
    navDropdown.forEach(el => {
      let dropdownMenu = el.nextElementSibling;
      if(btn === el) {
        dropdownMenu.classList.toggle('drop-collapse')
      } else {
        dropdownMenu.classList.remove('drop-collapse')
      }
    })  
  }
})
    
// Close the dropdown if the user clicks outside of it
window.onclick = e => {
  if (e.target.matches('.navbar-ul-drop') || e.target.matches('.arrow-down')) return
  drops.forEach(btn => btn.classList.remove('drop-collapse'))
}