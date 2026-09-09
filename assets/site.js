(function () {
    function clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }

    function sectionTitle(section) {
        return section.dataset.sectionTitle || 'Section';
    }

    function setStepParam(stepIndex) {
        const url = new URL(window.location.href);
        if (stepIndex <= 0) {
            url.searchParams.delete('step');
        } else {
            url.searchParams.set('step', String(stepIndex + 1));
        }
        window.history.replaceState({}, '', url);
    }

    function initialStep(totalSteps) {
        const params = new URLSearchParams(window.location.search);
        const rawStep = Number.parseInt(params.get('step') || '1', 10);
        if (Number.isNaN(rawStep)) {
            return 0;
        }
        return clamp(rawStep - 1, 0, totalSteps - 1);
    }

    function initPaginator(root) {
        const sections = Array.from(root.querySelectorAll('.page-section'));
        if (!sections.length) {
            return;
        }

        const previousButton = root.querySelector('[data-previous-button]');
        const nextButton = root.querySelector('[data-next-button]');
        const select = root.querySelector('[data-section-select]');
        const caption = root.querySelector('[data-step-caption]');
        const progressFill = root.querySelector('[data-progress-fill]');
        const previousWeekUrl = root.dataset.previousWeekUrl || '';
        const nextWeekUrl = root.dataset.nextWeekUrl || '';
        let currentStep = initialStep(sections.length);

        function update() {
            sections.forEach(function (section, index) {
                section.classList.toggle('active', index === currentStep);
                section.toggleAttribute('hidden', index !== currentStep);
            });

            if (caption) {
                caption.textContent = `Step ${currentStep + 1} of ${sections.length}`;
            }

            if (progressFill) {
                progressFill.style.width = `${((currentStep + 1) / sections.length) * 100}%`;
            }

            if (select) {
                select.value = String(currentStep);
            }

            if (previousButton) {
                if (currentStep > 0) {
                    previousButton.textContent = `Previous (${sectionTitle(sections[currentStep - 1])})`;
                    previousButton.disabled = false;
                } else if (previousWeekUrl) {
                    previousButton.textContent = 'Previous week';
                    previousButton.disabled = false;
                } else {
                    previousButton.textContent = 'Previous';
                    previousButton.disabled = true;
                }
            }

            if (nextButton) {
                if (currentStep < sections.length - 1) {
                    nextButton.textContent = `Next (${sectionTitle(sections[currentStep + 1])})`;
                    nextButton.disabled = false;
                } else if (nextWeekUrl) {
                    nextButton.textContent = 'Next week';
                    nextButton.disabled = false;
                } else {
                    nextButton.textContent = 'Next';
                    nextButton.disabled = true;
                }
            }

            setStepParam(currentStep);
        }

        if (previousButton) {
            previousButton.addEventListener('click', function () {
                if (currentStep > 0) {
                    currentStep -= 1;
                    update();
                } else if (previousWeekUrl) {
                    window.location.href = previousWeekUrl;
                }
            });
        }

        if (nextButton) {
            nextButton.addEventListener('click', function () {
                if (currentStep < sections.length - 1) {
                    currentStep += 1;
                    update();
                } else if (nextWeekUrl) {
                    window.location.href = nextWeekUrl;
                }
            });
        }

        if (select) {
            select.addEventListener('change', function () {
                currentStep = clamp(Number.parseInt(select.value, 10), 0, sections.length - 1);
                update();
            });
        }

        update();
    }

    function initSidebarToggle() {
        const toggle = document.querySelector('.sidebar-toggle');
        if (!toggle) {
            return;
        }
        toggle.addEventListener('click', function () {
            const isOpen = document.body.classList.toggle('sidebar-open');
            toggle.setAttribute('aria-expanded', String(isOpen));
        });
    }

    function pdfjsBaseUrl() {
        const script = document.querySelector('script[src*="site.js"]');
        if (!script) {
            return 'assets/pdfjs/';
        }
        return script.getAttribute('src').replace(/site\.js([?#].*)?$/, 'pdfjs/');
    }

    function loadPdfJs(baseUrl) {
        return new Promise(function (resolve, reject) {
            if (window.pdfjsLib) {
                resolve(window.pdfjsLib);
                return;
            }
            const script = document.createElement('script');
            script.src = baseUrl + 'pdf.min.js';
            script.onload = function () {
                if (!window.pdfjsLib) {
                    reject(new Error('pdf.min.js loaded but pdfjsLib is undefined'));
                    return;
                }
                window.pdfjsLib.GlobalWorkerOptions.workerSrc = baseUrl + 'pdf.worker.min.js';
                resolve(window.pdfjsLib);
            };
            script.onerror = function () {
                reject(new Error('Failed to load PDF.js'));
            };
            document.head.appendChild(script);
        });
    }

    function initSlideReader() {
        const buttons = Array.from(document.querySelectorAll('[data-slide-reader]'));
        const overlay = document.querySelector('[data-slide-reader-overlay]');
        if (!buttons.length || !overlay) {
            return;
        }
        const canvas = overlay.querySelector('[data-slide-reader-canvas]');
        const countEl = overlay.querySelector('[data-slide-reader-count]');
        const closeBtn = overlay.querySelector('[data-slide-reader-close]');
        const prevBtn = overlay.querySelector('[data-slide-reader-prev]');
        const nextBtn = overlay.querySelector('[data-slide-reader-next]');

        let pdfDoc = null;
        let currentPage = 0;
        let pageCount = 0;

        function renderPage() {
            if (!pdfDoc) {
                return;
            }
            Promise.resolve(pdfDoc.getPage(currentPage)).then(function (page) {
                const viewport = page.getViewport({ scale: 1 });
                const scale = Math.min(
                    (canvas.clientWidth - 40) / viewport.width,
                    (canvas.clientHeight - 40) / viewport.height,
                    2
                );
                const vp = page.getViewport({ scale: Math.max(scale, 0.1) });
                canvas.width = vp.width;
                canvas.height = vp.height;
                const ctx = canvas.getContext('2d');
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, vp.width, vp.height);
                page.render({ canvasContext: ctx, viewport: vp }).promise.catch(function () {});
            });
        }

        function updateControls() {
            if (countEl) {
                countEl.textContent = currentPage + ' / ' + pageCount;
            }
            if (prevBtn) {
                prevBtn.disabled = currentPage <= 1;
            }
            if (nextBtn) {
                nextBtn.disabled = currentPage >= pageCount;
            }
        }

        function setCurrentPage(pageNum) {
            currentPage = clamp(pageNum, 1, pageCount);
            renderPage();
            updateControls();
        }

        function show() {
            overlay.hidden = false;
            overlay.setAttribute('aria-hidden', 'false');
            document.body.classList.add('slide-reader-open');
        }

        function hide() {
            overlay.hidden = true;
            overlay.setAttribute('aria-hidden', 'true');
            document.body.classList.remove('slide-reader-open');
        }

        buttons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                const pdfUrl = btn.getAttribute('data-slide-pdf');
                if (!pdfUrl) {
                    return;
                }
                show();
                pdfDoc = null;
                loadPdfJs(pdfjsBaseUrl())
                    .then(function (pdfjs) {
                        return pdfjs.getDocument(pdfUrl).promise;
                    })
                    .then(function (doc) {
                        pdfDoc = doc;
                        pageCount = doc.numPages;
                        setCurrentPage(1);
                    })
                    .catch(function (err) {
                        if (countEl) {
                            countEl.textContent = 'Unable to load slides';
                        }
                        console.error('Slide reader error:', err);
                    });
            });
        });

        if (prevBtn) {
            prevBtn.addEventListener('click', function () {
                setCurrentPage(currentPage - 1);
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', function () {
                setCurrentPage(currentPage + 1);
            });
        }
        if (closeBtn) {
            closeBtn.addEventListener('click', hide);
        }
        window.addEventListener('resize', renderPage);
        document.addEventListener('keydown', function (event) {
            if (overlay.hidden) {
                return;
            }
            if (event.key === 'Escape') {
                hide();
            } else if (event.key === 'ArrowRight') {
                setCurrentPage(currentPage + 1);
            } else if (event.key === 'ArrowLeft') {
                setCurrentPage(currentPage - 1);
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-paginator]').forEach(initPaginator);
        initSidebarToggle();
        initSlideReader();
    });
})();
