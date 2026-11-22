const menuButton = document.querySelector('.menu-toggle')
const navLinks = document.querySelector('.nav-links')

function setMenu(open) {
  navLinks.classList.toggle('open', open)
  menuButton.setAttribute('aria-expanded', String(open))
  menuButton.textContent = open ? 'Close' : 'Menu'
}

if (menuButton && navLinks) {
  document.documentElement.classList.add('enhanced')
  menuButton.addEventListener('click', (event) => {
    const open = menuButton.getAttribute('aria-expanded') === 'false'
    setMenu(open)
    if (open && event.detail === 0) navLinks.querySelector('a')?.focus()
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
  document.addEventListener('focusin', (event) => {
    if (!event.target.closest('.nav') && menuButton.getAttribute('aria-expanded') === 'true') {
      setMenu(false)
    }
  })
  window.matchMedia('(min-width: 961px)').addEventListener('change', () => setMenu(false))
}

const pageSections = document.querySelectorAll('.detail-subnav a[href^="#"]')
if (pageSections.length) {
  const markSection = () => {
    for (const anchor of pageSections) {
      if (anchor.hash === window.location.hash) anchor.setAttribute('aria-current', 'location')
      else anchor.removeAttribute('aria-current')
    }
  }
  markSection()
  window.addEventListener('hashchange', markSection)
}

const date = document.querySelector('#visit-date')
if (date) {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  date.min = `${year}-${month}-${day}`
}

const requestedProgramme = new URLSearchParams(window.location.search).get('programme')
for (const form of document.querySelectorAll('.visit-form')) {
  form.hidden = false
  const phone = form.elements.phone
  const course = form.elements.course
  if (requestedProgramme && !course.value) {
    const match = Array.from(course.options).find((option) => option.dataset.programme === requestedProgramme)
    if (match) course.value = match.value
  }
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
