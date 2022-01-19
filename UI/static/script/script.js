'use strict';

const modal1 = document.querySelector('#modal1');
const modal2 = document.querySelector('#modal2');
const modal3 = document.querySelector('#modal3');
const modal4 = document.querySelector('#modal4');
const modal5 = document.querySelector('#modal5');
const overlay = document.querySelector('.overlay');
const signOutForm = document.querySelector('#signoutForm');
const profileForm = document.querySelector('#profileForm');
const signInBtn = document.querySelector('#signin');
const signOutBtn = document.querySelector('#signout');
const signUpBtn = document.querySelectorAll('#signup');
const profileBtn = document.querySelector('#profile');
const addFundsBtn = document.querySelector('#addFunds');
const convertFundsBtn = document.querySelector('#convertFunds');
const sendFundsBtn = document.querySelector('#sendFunds');
const btnCloseModal = document.querySelectorAll('.btn--close-modal');
const nav = document.querySelector('.nav');

///////////////////////////////////////
// Modal window

const openModal = function (modal) {
  const e = window.event;
  modal.hidden = false;
  overlay.hidden = false;
};

const closeModal = function () {
  if (!modal1.hidden) modal1.hidden = true;
  else if (!modal2.hidden) modal2.hidden = true;
  else if (!modal3.hidden) modal3.hidden = true;
  else if (!modal4.hidden) modal4.hidden = true;
  else if (!modal5.hidden) modal5.hidden = true;
  overlay.hidden = true;
};

////////////////////////////////////////
if (signUpBtn) {
  signUpBtn.forEach(btn =>
    btn.addEventListener('click', openModal.bind(this, modal1))
  );
}

if (signOutBtn) {
  signOutBtn.addEventListener('click', e => {
    signOutForm.submit();
  });
}

if (profileBtn) {
  profileBtn.addEventListener('click', e => {
    profileForm.submit();
  });
}

/////////////////////////
if (signInBtn) {
  signInBtn.addEventListener('click', openModal.bind(this, modal2));
}
if (addFundsBtn) {
  addFundsBtn.addEventListener('click', openModal.bind(this, modal3));
}
if (convertFundsBtn) {
  convertFundsBtn.addEventListener('click', openModal.bind(this, modal4));
}
if (sendFundsBtn) {
  sendFundsBtn.addEventListener('click', openModal.bind(this, modal5));
}

btnCloseModal.forEach(btn => btn.addEventListener('click', closeModal));

if (overlay) {
  overlay.addEventListener('click', e => {
    if (!modal1.hidden) closeModal();
    else if (!modal2.hidden) closeModal();
    else if (!modal3.hidden) closeModal();
    else if (!modal4.hidden) closeModal();
    else if (!modal5.hidden) closeModal();
  });
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && !modal1.hidden) {
    closeModal(modal1);
  } else if (e.key === 'Escape' && !modal2.hidden) {
    closeModal(modal2);
  } else if (e.key === 'Escape' && !modal3.hidden) {
    closeModal(modal3);
  } else if (e.key === 'Escape' && !modal4.hidden) {
    closeModal(modal4);
  } else if (e.key === 'Escape' && !modal5.hidden) {
    closeModal(modal5);
  }
});

///////////////////////////////////////
// Menu fade animation
const handleHover = function (e) {
  if (e.target.classList.contains('nav__link')) {
    const link = e.target;
    const siblings = link.closest('.nav').querySelectorAll('.nav__link');
    const logo = link.closest('.nav').querySelector('img');

    siblings.forEach(el => {
      if (el !== link) el.style.opacity = this;
    });
    logo.style.opacity = this;
  }
};

// Passing "argument" into handler
nav.addEventListener('mouseover', handleHover.bind(0.5));
nav.addEventListener('mouseout', handleHover.bind(1));
