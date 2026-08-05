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

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-paginator]').forEach(initPaginator);
        initSidebarToggle();
    });
})();
