document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('btn-toggle-categorias');
    const categoriasSidebar = document.getElementById('categorias-sidebar-nav');
    const mainNavigation = document.getElementById('main-navigation');
    const mainContentOverlay = document.querySelector('.main-content-overlay');

    function updateToggleButton(isMenuOpen) {
        if (toggleButton) {
            toggleButton.innerHTML = isMenuOpen ? '&times;' : '&#9776;';
            toggleButton.setAttribute('aria-expanded', isMenuOpen);
        }
    }

    function openMenu(menuElement) {
        if (!menuElement) return;
        if (menuElement.id === 'categorias-sidebar-nav') {
            menuElement.classList.add('is-active');
        } else if (menuElement.id === 'main-navigation') {
            menuElement.classList.add('main-nav-open');
        }
        document.body.classList.add('sidebar-is-active');
        updateToggleButton(true);
    }

    function closeAllMenus() {
        if (categoriasSidebar) categoriasSidebar.classList.remove('is-active');
        if (mainNavigation) mainNavigation.classList.remove('main-nav-open');
        document.body.classList.remove('sidebar-is-active');
        updateToggleButton(false);
    }

    if (toggleButton) {
        toggleButton.addEventListener('click', function(e) {
            e.stopPropagation();
            const isHomePage = window.location.pathname === '/';
            const targetMenu = isHomePage ? mainNavigation : categoriasSidebar;
            const isOpen = targetMenu.classList.contains('is-active') || targetMenu.classList.contains('main-nav-open');

            if (isOpen) {
                closeAllMenus();
            } else {
                closeAllMenus(); // Cierra cualquier otro menú abierto
                openMenu(targetMenu);
            }
        });
    }

    if (mainContentOverlay) {
        mainContentOverlay.addEventListener('click', closeAllMenus);
    }

   // --- Lógica para el Acordeón de Categorías (Versión Simple Refinada) ---
const categoryLinks = document.querySelectorAll('.categorias-sidebar .has-submenu > .cat-principal-link');

categoryLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        // Prevenir la navegación para que el clic solo abra/cierre el menú
        event.preventDefault(); 

        const parentLi = this.parentElement;
        parentLi.classList.toggle('open');

        // --- AÑADIDO: Lógica para cambiar el ícono ---
        const toggleIcon = this.querySelector('.submenu-toggle');
        if (toggleIcon) {
            if (parentLi.classList.contains('open')) {
                toggleIcon.textContent = '−'; // Signo de menos cuando está abierto
            } else {
                toggleIcon.textContent = '+'; // Signo de más cuando está cerrado
            }
        }
        // --- FIN DEL AÑADIDO ---
    });
});

    // --- Lógica para el Modal de Imagen Ampliada ---
    const mainProductImageDisplay = document.getElementById('main-product-image-display');
    const imageModal = document.getElementById('image-modal');
    const modalImageSrc = document.getElementById('modal-image-src');
    const closeModalButton = imageModal ? imageModal.querySelector('.image-modal-close') : null;

    if (mainProductImageDisplay && imageModal && modalImageSrc && closeModalButton) {
        mainProductImageDisplay.addEventListener('click', function() {
            if (this.src && !this.src.includes('via.placeholder.com')) {
                modalImageSrc.src = this.src;
                imageModal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });

        const closeImageModal = () => {
            imageModal.classList.remove('active');
            document.body.style.overflow = 'auto';
            setTimeout(() => { modalImageSrc.src = ""; }, 300);
        };

        closeModalButton.addEventListener('click', closeImageModal);
        imageModal.addEventListener('click', (event) => {
            if (event.target === imageModal) closeImageModal();
        });
    }

    // --- Lógica de la Galería de Miniaturas ---
    const thumbnailImages = document.querySelectorAll('.thumbnail-image');
    if (mainProductImageDisplay && thumbnailImages.length > 0) {
        thumbnailImages.forEach(thumb => {
            thumb.addEventListener('click', function() {
                mainProductImageDisplay.src = this.dataset.fullimageUrl;
                thumbnailImages.forEach(img => img.classList.remove('active-thumbnail'));
                this.classList.add('active-thumbnail');
            });
        });
    }

    // --- Lógica para el Modal de Términos y Condiciones ---
    const openTermsModalLink = document.getElementById('open-terms-modal-link');
    const termsConditionsModal = document.getElementById('terms-conditions-modal');
    const closeTermsModalButton = termsConditionsModal ? termsConditionsModal.querySelector('.modal-close-terms') : null;
    const acceptTermsFromModalButton = document.getElementById('accept-terms-from-modal');
    const aceptaTerminosCheckbox = document.getElementById('acepta_terminos');

    if (openTermsModalLink && termsConditionsModal && closeTermsModalButton && aceptaTerminosCheckbox && acceptTermsFromModalButton) {
        openTermsModalLink.addEventListener('click', function(event) {
            event.preventDefault();
            termsConditionsModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        const closeTermsModal = () => {
            termsConditionsModal.classList.remove('active');
            document.body.style.overflow = 'auto';
        };

        closeTermsModalButton.addEventListener('click', closeTermsModal);
        acceptTermsFromModalButton.addEventListener('click', () => {
            aceptaTerminosCheckbox.checked = true;
            closeTermsModal();
        });
        termsConditionsModal.addEventListener('click', (event) => {
            if (event.target === termsConditionsModal) closeTermsModal();
        });
    }

    // --- Lógica para el campo de WhatsApp en el formulario de crédito ---
    const tieneWhatsappCheckbox = document.getElementById('tiene_whatsapp');
    const whatsappOtroGroup = document.getElementById('whatsapp_otro_group');
    if (tieneWhatsappCheckbox && whatsappOtroGroup) {
        const whatsappOtroInput = document.getElementById('whatsapp_otro');
        function toggleWhatsappOtro() {
            if (tieneWhatsappCheckbox.checked) {
                whatsappOtroGroup.style.display = 'none';
                if(whatsappOtroInput) whatsappOtroInput.value = '';
            } else {
                whatsappOtroGroup.style.display = 'block';
            }
        }
        toggleWhatsappOtro();
        tieneWhatsappCheckbox.addEventListener('change', toggleWhatsappOtro);
    }

    // --- Inicializar Tiny Slider ---
    const carouselContainer = document.querySelector('.carousel-items');
    if (carouselContainer) {
        tns({
            container: '.carousel-items',
            items: 1,
            slideBy: 'page',
            autoplay: true,
            autoplayButtonOutput: false,
            mouseDrag: true,
            controls: false, 
            nav: false,      
            autoplayTimeout: 5000,
            gutter: 0,
            responsive: {
                600: { items: 2, gutter: 10 },
                900: { items: 3, gutter: 15 },
                1200: { items: 4, gutter: 20 }
            }
        });
    }
});