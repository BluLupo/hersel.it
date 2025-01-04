const blackHole = document.querySelector('.black-hole');

blackHole.addEventListener('mouseover', () => {
  blackHole.style.transform = 'scale(1.2)';
  blackHole.style.transition = 'transform 0.2s ease';
});

blackHole.addEventListener('mouseout', () => {
  blackHole.style.transform = 'scale(1)';
});
