const menuButton = document.querySelector('.menu-toggle')
const navLinks = document.querySelector('.nav-links')

function setMenu(open) {
  navLinks.classList.toggle('open', open)
  menuButton.setAttribute('aria-expanded', String(open))
  menuButton.textContent = open ? 'Close' : 'Menu'
}

if (menuButton && navLinks) {
  document.documentElement.classList.add('enhanced')
  menuButton.addEventListener('click', () => {
    setMenu(menuButton.getAttribute('aria-expanded') === 'false')
  })
  navLinks.addEventListener('click', (event) => {
    if (event.target.closest('a')) setMenu(false)
  })
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      setMenu(false)
      menuButton.focus()
    }
  })
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.nav') && menuButton.getAttribute('aria-expanded') === 'true') {
      setMenu(false)
    }
  })
  window.matchMedia('(min-width: 961px)').addEventListener('change', () => setMenu(false))
}

const date = document.querySelector('#visit-date')
if (date) {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  date.min = `${year}-${month}-${day}`
}

for (const form of document.querySelectorAll('.visit-form')) {
  form.hidden = false
  const phone = form.elements.phone
  const notice = form.querySelector('.form-message')
  phone.addEventListener('input', () => phone.setCustomValidity(''))
  form.addEventListener('submit', (event) => {
    event.preventDefault()
    const enteredPhone = phone.value.trim()
    const number = enteredPhone.replace(/\D/g, '')
    if (!/^\+?[\d\s().-]+$/.test(enteredPhone) || number.length < 10 || number.length > 15) {
      phone.setCustomValidity('Please check your phone number so we can reach you.')
      phone.reportValidity()
      return
    }

    const values = new FormData(form)
    const lines = [
      form.dataset.message,
      `Name: ${values.get('name').trim()}`,
      `Phone: ${enteredPhone}`,
      `I am a: ${values.get('role')}`,
      `Programme: ${values.get('course')}`
    ]
    if (values.get('date')) {
      const preferred = new Date(`${values.get('date')}T12:00:00`)
      const display = new Intl.DateTimeFormat('en-IN', { dateStyle: 'long' }).format(preferred)
      lines.push(`Preferred date: ${display}`)
    }

    notice.textContent = 'Your draft is ready in WhatsApp. Send it there to contact the admissions team.'
    window.location.assign(`https://wa.me/919000719444?text=${encodeURIComponent(lines.join('\n'))}`)
  })
}
