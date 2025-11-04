const elementosDuvida = document.querySelectorAll(".duvida");

elementosDuvida.forEach((duvida) => {
  duvida.addEventListener("click", () => {
        elementosDuvida.forEach( (outraDuvida) => {
            if (outraDuvida !== duvida) {
              outraDuvida.classList.remove("ativa");
            }
        });
    duvida.classList.toggle("ativa");
  });
});


document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.flash-message');
    const displayTime = 2000;

    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';

            setTimeout(() => {
                message.remove();
            }, 500);

        }, displayTime);
    });
});