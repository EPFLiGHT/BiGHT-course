(function () {
    function clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }

    function sectionTitle(section) {
        return section.dataset.sectionTitle || 'Section';
    }

    function setStepParam(stepIndex, all, legacySteps) {
        const url = new URL(window.location.href);
        const param = legacySteps.length ? 'section' : 'step';
        if (legacySteps.length) url.searchParams.delete('step');
        if (stepIndex <= 0) {
            url.searchParams.delete(param);
        } else {
            url.searchParams.set(param, String(stepIndex + 1));
        }
        if (all) url.searchParams.set('view', 'all');
        else url.searchParams.delete('view');
        url.hash = all ? '' : `section-${stepIndex + 1}`;
        window.history.pushState({}, '', url);
    }

    function initialStep(totalSteps, legacySteps) {
        const params = new URLSearchParams(window.location.search);
        const hash = window.location.hash.match(/^#section-(\d+)$/);
        const legacyStep = Number.parseInt(params.get('step'), 10);
        const mappedStep = legacySteps[legacyStep - 1] || legacyStep;
        const rawStep = Number.parseInt(params.get('section') || mappedStep || (hash && hash[1]) || '1', 10);
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
        const legacySteps = JSON.parse(root.dataset.legacySteps || '[]');
        let currentStep = initialStep(sections.length, legacySteps);
        let all = new URLSearchParams(window.location.search).get('view') === 'all';
        const viewAll = root.querySelector('[data-view-all]');
        const links = Array.from(root.querySelectorAll('[data-section-link]'));

        function scrollToLegacySection() {
            const params = new URLSearchParams(window.location.search);
            if (!legacySteps.length || params.has('section')) return;
            const step = Number.parseInt(params.get('step'), 10);
            const anchor = document.getElementById(`legacy-step-${step}`);
            if (anchor) requestAnimationFrame(() => anchor.scrollIntoView({ block: 'start' }));
        }

        function update() {
            sections.forEach(function (section, index) {
                section.classList.toggle('active', all || index === currentStep);
                section.toggleAttribute('hidden', !all && index !== currentStep);
            });

            var activeReader = sections[currentStep]
                && sections[currentStep].querySelector('[data-slide-reader]');
            if (activeReader && activeReader._pdf) {
                renderSlide(activeReader);
            }

            if (caption) {
                caption.textContent = all ? `All ${sections.length} sections` : `Section ${currentStep + 1} of ${sections.length}`;
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

            links.forEach(function (link, index) {
                if (!all && index === currentStep) link.setAttribute('aria-current', 'location');
                else link.removeAttribute('aria-current');
            });
            if (viewAll) {
                viewAll.textContent = all ? 'Show one section at a time' : 'Show entire week on one page';
                viewAll.setAttribute('aria-pressed', String(all));
            }
        }

        function go(index) {
            currentStep = index;
            all = false;
            setStepParam(currentStep, all, legacySteps);
            update();
            sections[currentStep].focus({ preventScroll: true });
            window.scrollTo({ top: 0, left: 0 });
        }

        if (previousButton) {
            previousButton.addEventListener('click', function () {
                if (currentStep > 0) {
                    go(currentStep - 1);
                } else if (previousWeekUrl) {
                    window.location.href = previousWeekUrl;
                }
            });
        }

        if (nextButton) {
            nextButton.addEventListener('click', function () {
                if (currentStep < sections.length - 1) {
                    go(currentStep + 1);
                } else if (nextWeekUrl) {
                    window.location.href = nextWeekUrl;
                }
            });
        }

        if (select) {
            select.addEventListener('change', function () {
                go(clamp(Number.parseInt(select.value, 10), 0, sections.length - 1));
            });
        }

        links.forEach(function (link, index) {
            link.addEventListener('click', function (event) {
                if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
                event.preventDefault();
                if (!root.classList.contains('week-overview') || !window.matchMedia('(min-width: 1201px)').matches) link.closest('details').open = false;
                if (all && root.classList.contains('week-overview')) {
                    currentStep = index;
                    const url = new URL(window.location.href);
                    if (legacySteps.length) url.searchParams.delete('step');
                    url.searchParams.set(legacySteps.length ? 'section' : 'step', String(index + 1));
                    url.hash = sections[index].id;
                    window.history.pushState({}, '', url);
                    update();
                    sections[index].focus({ preventScroll: true });
                    sections[index].scrollIntoView({ block: 'start' });
                } else {
                    go(index);
                }
            });
        });
        if (viewAll) viewAll.addEventListener('click', function () {
            all = !all;
            setStepParam(currentStep, all, legacySteps);
            update();
        });
        window.addEventListener('popstate', function () {
            currentStep = initialStep(sections.length, legacySteps);
            all = new URLSearchParams(window.location.search).get('view') === 'all';
            update();
            scrollToLegacySection();
        });
        update();
        scrollToLegacySection();
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
            if (document.fullscreenElement === readers) {
                var wrapHeight = wrap.clientHeight || 900;
                scale = Math.min(scale, (wrapHeight - 60) / viewport.height);
            }
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
        var fsButton = reader.querySelector('[data-slide-reader-fullscreen]');
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
        if (fsButton) {
            var fsText = fsButton.querySelector('.slide-reader-fs-text');
            function isFullscreen() {
                return !!(document.fullscreenElement && document.fullscreenElement === reader);
            }
            function updateFullscreenState() {
                var on = isFullscreen();
                fsButton.classList.toggle('is-fullscreen', on);
                fsButton.setAttribute('aria-pressed', on ? 'true' : 'false');
                if (on) {
                    fsButton.setAttribute('aria-label', 'Exit full screen');
                    if (fsText) { fsText.textContent = 'Exit full screen'; }
                } else {
                    fsButton.setAttribute('aria-label', 'Show slides full screen');
                    if (fsText) { fsText.textContent = 'Full screen'; }
                }
                if (reader._pdf) {
                    requestAnimationFrame(function () {
                        requestAnimationFrame(function () {
                            renderSlide(reader);
                        });
                    });
                }
            }
            fsButton.addEventListener('click', function () {
                if (document.fullscreenElement) {
                    if (document.exitFullscreen) {
                        document.exitFullscreen();
                    }
                } else if (reader.requestFullscreen) {
                    reader.requestFullscreen();
                }
            });
            document.addEventListener('fullscreenchange', updateFullscreenState);
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

    function zurichNow() {
        const parts = new Intl.DateTimeFormat('en-CA', {
            timeZone: 'Europe/Zurich', year: 'numeric', month: '2-digit', day: '2-digit',
            hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
        }).formatToParts(new Date());
        const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
        return `${values.year}-${values.month}-${values.day}T${values.hour}:${values.minute}`;
    }

    function sameCalendarWeek(left, right) {
        function monday(value) {
            const date = new Date(value.slice(0, 10) + 'T00:00:00Z');
            date.setUTCDate(date.getUTCDate() - (date.getUTCDay() + 6) % 7);
            return date.getTime();
        }
        return monday(left) === monday(right);
    }

    function initCalendar() {
        const now = zurichNow();
        document.querySelectorAll('[data-week-date]').forEach(function (item) {
            if (sameCalendarWeek(item.dataset.weekDate, now)) item.querySelector('.calendar-week-label').hidden = false;
        });
        const root = document.querySelector('[data-student-tools]');
        if (!root) return;
        const weeks = JSON.parse(root.dataset.weeks);
        const current = weeks.find(week => sameCalendarWeek(week.date, now));
        const target = root.querySelector('[data-current-week]');
        if (current) {
            target.textContent = `Current calendar week: `;
            if (current.url) {
                const link = document.createElement('a');
                link.href = current.url;
                link.textContent = `Week ${current.week}`;
                target.append(' ', link);
            } else target.append(` — ${current.release_label}`);
        } else if (now.slice(0, 10) < weeks[0].date) target.textContent = 'The teaching semester has not started yet.';
        else if (now.slice(0, 10) > weeks[weeks.length - 1].date) target.textContent = 'The teaching semester has ended.';
        else target.textContent = 'There is no scheduled teaching week this calendar week.';
        const events = JSON.parse(root.dataset.events).filter(event => event.when >= now).slice(0, 3);
        const upcoming = root.querySelector('[data-upcoming]');
        const text = upcoming.querySelector('p');
        if (events.length) {
            const list = document.createElement('ul');
            events.forEach(function (event) {
                const item = document.createElement('li');
                const link = document.createElement('a');
                link.href = event.href || `project-documentation/student/?step=${event.step}`;
                link.textContent = event.label;
                item.append(`${event.date} - `, link);
                list.append(item);
            });
            text.replaceWith(list);
        } else text.textContent = 'No upcoming dated deadlines or assessments in the project timeline.';
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-paginator]').forEach(initPaginator);
        document.querySelectorAll('.unpaginated .section-menu a').forEach(function (link) {
            link.addEventListener('click', function () { link.closest('details').open = false; });
        });
        const legacy = document.querySelector('.pagination-shell.unpaginated');
        const step = Number.parseInt(new URLSearchParams(location.search).get('step'), 10);
        if (legacy && step > 0) {
            const section = legacy.querySelectorAll('.section')[step - 1];
            if (section) section.scrollIntoView();
        }
        initCalendar();
        initSidebarToggle();
        initSlideReaders();
    });
})();
