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

            var activeReader = sections[currentStep]
                && sections[currentStep].querySelector('[data-slide-reader]');
            if (activeReader && activeReader._pdf) {
                renderSlide(activeReader);
            }

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
        function setOpen(isOpen) {
            document.body.classList.toggle('sidebar-open', isOpen);
            toggle.textContent = isOpen ? 'Close' : 'Menu';
            toggle.setAttribute('aria-expanded', String(isOpen));
        }
        toggle.addEventListener('click', function () {
            setOpen(!document.body.classList.contains('sidebar-open'));
        });
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && document.body.classList.contains('sidebar-open')) {
                setOpen(false);
                toggle.focus();
            }
        });
    }

    function pdfjsBaseUrl() {
        var src = '';
        var scripts = document.getElementsByTagName('script');
        for (var i = 0; i < scripts.length; i += 1) {
            var s = scripts[i];
            if (s.src && /\/site\.js/.test(s.src)) {
                src = s.src.substring(0, s.src.lastIndexOf('/') + 1) + 'pdfjs/';
                break;
            }
        }
        return src;
    }

    function loadPdfJs() {
        if (window.PDFJS_LOADED) {
            return Promise.resolve();
        }
        var base = pdfjsBaseUrl();
        var js = document.createElement('script');
        var worker = document.createElement('script');
        var scriptLoad = new Promise(function (resolve) {
            js.onload = resolve;
            js.onerror = resolve;
            js.src = base + 'pdf.min.js';
        });
        var workerLoad = new Promise(function (resolve) {
            worker.onload = resolve;
            worker.onerror = resolve;
            worker.src = base + 'pdf.worker.min.js';
        });
        document.head.appendChild(js);
        document.head.appendChild(worker);
        return Promise.all([scriptLoad, workerLoad]).then(function () {
            if (window.pdfjsLib) {
                window.pdfjsLib.GlobalWorkerOptions.workerSrc = base + 'pdf.worker.min.js';
                window.PDFJS_LOADED = true;
            }
        });
    }

    function renderSlide(readers) {
        var pdf = readers._pdf;
        if (!pdf) {
            return;
        }
        var canvas = readers.querySelector('[data-slide-reader-canvas]');
        var count = readers.querySelector('[data-slide-reader-count]');
        var gotoInput = readers.querySelector('[data-slide-reader-goto]');
        var pageNum = readers._page;
        if (readers._renderTask) {
            try {
                readers._renderTask.cancel();
            } catch (e) { /* already finished */ }
            readers._renderTask = null;
        }
        pdf.getPage(pageNum).then(function (page) {
            var wrap = canvas.parentElement;
            var wrapWidth = wrap.clientWidth || 800;
            var cap = 1100;
            var viewport = page.getViewport({ scale: 1 });
            var scale = Math.min((wrapWidth - 40) / viewport.width, cap / viewport.height, 2);
            if (scale < 0.1) {
                scale = 0.1;
            }
            viewport = page.getViewport({ scale: scale });
            var ratio = window.devicePixelRatio || 1;
            canvas.width = Math.floor(viewport.width * ratio);
            canvas.height = Math.floor(viewport.height * ratio);
            canvas.style.width = Math.floor(viewport.width) + 'px';
            canvas.style.height = Math.floor(viewport.height) + 'px';
            var context = canvas.getContext('2d');
            context.setTransform(ratio, 0, 0, ratio, 0, 0);
            var task = page.render({ canvasContext: context, viewport: viewport });
            readers._renderTask = task;
            task.promise.then(function () {
                page.cleanup();
                if (readers._renderTask === task) {
                    readers._renderTask = null;
                }
            }).catch(function () {
                if (readers._renderTask === task) {
                    readers._renderTask = null;
                }
            });
        });
        if (gotoInput) {
            gotoInput.max = "" + readers._total;
            gotoInput.value = "" + pageNum;
        }
        if (count) {
            count.textContent = 'of ' + readers._total;
        }
    }

    function goSlide(readers, delta) {
        var next = readers._page + delta;
        if (next < 1 || next > readers._total) {
            return;
        }
        readers._page = next;
        renderSlide(readers);
    }

    function goToSlide(readers, target) {
        var num = Number.parseInt(target, 10);
        if (Number.isNaN(num)) {
            return;
        }
        readers._page = clamp(num, 1, readers._total);
        renderSlide(readers);
    }

    function initSlideReader(reader) {
        var pdfUrl = reader.getAttribute('data-slide-pdf');
        if (!pdfUrl || !window.pdfjsLib) {
            return;
        }
        var prev = reader.querySelector('[data-slide-reader-prev]');
        var next = reader.querySelector('[data-slide-reader-next]');
        var gotoInput = reader.querySelector('[data-slide-reader-goto]');
        reader._page = 1;
        reader._total = 1;
        window.pdfjsLib.getDocument(pdfUrl).promise.then(function (pdf) {
            reader._pdf = pdf;
            reader._total = pdf.numPages;
            renderSlide(reader);
        });
        function isSectionActive() {
            var section = reader.closest('.page-section');
            return !section || section.classList.contains('active');
        }
        if (prev) {
            prev.addEventListener('click', function () { goSlide(reader, -1); });
        }
        if (next) {
            next.addEventListener('click', function () { goSlide(reader, 1); });
        }
        if (gotoInput) {
            function jumpFromInput() {
                goToSlide(reader, gotoInput.value);
            }
            gotoInput.addEventListener('focus', function () {
                gotoInput.select();
            });
            gotoInput.addEventListener('change', jumpFromInput);
            gotoInput.addEventListener('keydown', function (event) {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    jumpFromInput();
                    gotoInput.blur();
                }
            });
        }
        function onKey(event) {
            if (gotoInput && document.activeElement === gotoInput) {
                return;
            }
            if (event.key === 'ArrowLeft') {
                goSlide(reader, -1);
                event.preventDefault();
            } else if (event.key === 'ArrowRight') {
                goSlide(reader, 1);
                event.preventDefault();
            }
        }
        reader._onKey = function (event) {
            if (isSectionActive()) {
                onKey(event);
            }
        };
        document.addEventListener('keydown', reader._onKey);
    }

    function initSlideReaders() {
        var readers = document.querySelectorAll('[data-slide-reader]');
        if (!readers.length) {
            return;
        }
        if (window.pdfjsLib) {
            readers.forEach(initSlideReader);
            return;
        }
        loadPdfJs().then(function () {
            if (!window.pdfjsLib) {
                return;
            }
            readers.forEach(initSlideReader);
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-paginator]').forEach(initPaginator);
        initSidebarToggle();
        initSlideReaders();
    });
})();
