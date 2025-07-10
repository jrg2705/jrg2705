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
        if (menuElement) menuElement.classList.add('is-active'); // Para sidebar
        if (menuElement === mainNavigation && mainNavigation) mainNavigation.classList.add('main-nav-open'); // Para main-nav

        if (document.body) document.body.classList.add('sidebar-is-active'); // Usamos la misma clase para el overlay
        updateToggleButton(true);
    }

    function closeAllMenus() {
        if (categoriasSidebar) categoriasSidebar.classList.remove('is-active');
        if (mainNavigation) mainNavigation.classList.remove('main-nav-open');

        if (document.body) document.body.classList.remove('sidebar-is-active');
        updateToggleButton(false);
    }

    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            const isHomePage = window.location.pathname === '/';

            if (isHomePage && mainNavigation) {
                const isMainMenuOpen = mainNavigation.classList.contains('main-nav-open');
                if (isMainMenuOpen) {
                    closeAllMenus();
                } else {
                    closeAllMenus(); // Cerrar cualquier otro menú primero
                    openMenu(mainNavigation);
                    if (toggleButton) toggleButton.setAttribute('aria-controls', 'main-navigation');
                }
            } else if (categoriasSidebar) {
                const isSidebarOpen = categoriasSidebar.classList.contains('is-active');
                if (isSidebarOpen) {
                    closeAllMenus();
                } else {
                    closeAllMenus(); // Cerrar cualquier otro menú primero
                    openMenu(categoriasSidebar);
                    if (toggleButton) toggleButton.setAttribute('aria-controls', 'categorias-sidebar-nav');
                }
            }
        });
    }

    // --- Lógica para el Modal de Imagen Ampliada y Galería de Miniaturas ---
    const mainProductImageDisplay = document.getElementById('main-product-image-display'); // Actualizado ID
    const imageModal = document.getElementById('image-modal');
    const modalImageSrc = document.getElementById('modal-image-src');
    const closeModalButton = imageModal ? imageModal.querySelector('.image-modal-close') : null;
    const thumbnailImages = document.querySelectorAll('.thumbnail-image');

    // Funcionalidad del Modal (Zoom)
    if (mainProductImageDisplay && imageModal && modalImageSrc && closeModalButton) {
        mainProductImageDisplay.addEventListener('click', function() {
            if (this.src && this.src.indexOf('via.placeholder.com') === -1) {
                imageModal.style.display = "flex";
                modalImageSrc.src = this.src; // Usar el src de la imagen principal actual
                document.body.style.overflow = 'hidden';
            }
        });

        closeModalButton.addEventListener('click', function() {
            imageModal.style.display = "none";
            document.body.style.overflow = 'auto';
        });

        imageModal.addEventListener('click', function(event) {
            if (event.target === imageModal) { // Si se hace clic en el fondo del modal
                imageModal.style.display = "none";
                document.body.style.overflow = 'auto';
            }
        });
    }

    // Funcionalidad de la Galería de Miniaturas
    if (mainProductImageDisplay && thumbnailImages.length > 0) {
        thumbnailImages.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                // Cambiar imagen principal
                mainProductImageDisplay.src = this.dataset.fullimageUrl;
                mainProductImageDisplay.alt = this.alt; // Actualizar alt text

                // Actualizar miniatura activa
                thumbnailImages.forEach(img => img.classList.remove('active-thumbnail'));
                this.classList.add('active-thumbnail');
            });
        });
    }
    // FIN Lógica para el Modal de Imagen Ampliada y Galería


    // --- Lógica para el Modal de Términos y Condiciones ---
    const openTermsModalLink = document.getElementById('open-terms-modal-link');
    const termsConditionsModal = document.getElementById('terms-conditions-modal');
    const closeTermsModalButton = document.getElementById('close-terms-modal-button');
    const acceptTermsFromModalButton = document.getElementById('accept-terms-from-modal');
    const aceptaTerminosCheckbox = document.getElementById('acepta_terminos'); // Asumiendo que el ID del checkbox es 'acepta_terminos' (Flask-WTF suele generarlo así)

    if (openTermsModalLink && termsConditionsModal && closeTermsModalButton && aceptaTerminosCheckbox && acceptTermsFromModalButton) {
        openTermsModalLink.addEventListener('click', function(event) {
            event.preventDefault(); // Prevenir el comportamiento por defecto del enlace
            termsConditionsModal.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Evitar scroll del fondo
        });

        function closeTermsModal() {
            termsConditionsModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }

        closeTermsModalButton.addEventListener('click', closeTermsModal);

        acceptTermsFromModalButton.addEventListener('click', function() {
            aceptaTerminosCheckbox.checked = true;
            closeTermsModal();
        });

        // Cerrar modal si se hace clic fuera del contenido
        termsConditionsModal.addEventListener('click', function(event) {
            if (event.target === termsConditionsModal) {
                closeTermsModal();
            }
        });
    }
    // FIN Lógica Modal Términos y Condiciones


    if (mainContentOverlay) {
        mainContentOverlay.addEventListener('click', function() {
            closeAllMenus();
        });
    }

    // Opcional: Cerrar el menú si se hace clic en un enlace dentro de él
    // Esto es más relevante para SPAs. Si los enlaces recargan la página, el menú se cerrará.
    // if (categoriasSidebar) {
    //     categoriasSidebar.addEventListener('click', function(event) {
    //         if (event.target.tagName === 'A' && categoriasSidebar.classList.contains('is-active')) {
    //             closeAllMenus();
    //         }
    //     });
    // }
    // if (mainNavigation) {
    //     mainNavigation.addEventListener('click', function(event) {
    //         if (event.target.tagName === 'A' && mainNavigation.classList.contains('main-nav-open')) {
    //             closeAllMenus();
    //         }
    //     });
    // }

    // }

    // Inicializar Tiny Slider para el carrusel de destacados
    const carouselContainer = document.querySelector('.carousel-items');
    if (carouselContainer) {
        var slider = tns({
            container: '.carousel-items',
            items: 1, // Items base para móviles
            slideBy: 'page',
            autoplay: true,
            autoplayButtonOutput: false,
            mouseDrag: true,
            controls: false,
            nav: false,
            autoplayTimeout: 5000, // Ajustado para movimiento más lento
            gutter: 0,
            responsive: {
                600: {
                    items: 2,
                    gutter: 10
                },
                900: { // A partir de 900px
                    items: 3,
                    gutter: 15
                },
                1200: { // A partir de 1200px
                    items: 4,
                    gutter: 20
                }
            }
        });
    }
});
