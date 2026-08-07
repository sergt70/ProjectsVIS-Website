/*
 * VIS Website
 * Common client-side functionality and registry-based multilingual content loading
 */

(function () {
    "use strict";

    const REGISTRY_FILENAME = "languages.json";

    const scriptUrl = document.currentScript
        ? document.currentScript.src
        : new URL("../assets/js/site.js", window.location.href).href;

    let languageRegistry = null;
    let enabledLanguages = [];
    let currentLanguageEntry = null;

    function buildI18nUrl(filename) {
        return new URL("../i18n/" + filename, scriptUrl).href;
    }

    async function fetchJson(url, errorLabel) {
        const response = await fetch(url, {
            cache: "no-store",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(
                errorLabel +
                ": " +
                response.status +
                " " +
                response.statusText
            );
        }

        return response.json();
    }

    function normalizeLanguageEntry(entry) {
        if (!entry || typeof entry !== "object") {
            return null;
        }

        const code = String(entry.code || "").trim().toLowerCase();
        const nativeName = String(
            entry.nativeName || entry.name || code
        ).trim();

        const path = String(
            entry.path || ("/" + code + "/")
        ).trim();

        const translationFile = String(
            entry.translationFile || (code + ".json")
        ).trim();

        if (!code || !nativeName || !translationFile) {
            return null;
        }

        return {
            code,
            locale: String(entry.locale || code).trim(),
            name: String(entry.name || nativeName).trim(),
            nativeName,
            direction: entry.direction === "rtl" ? "rtl" : "ltr",
            path: path.startsWith("/") ? path : "/" + path,
            translationFile,
            enabled: entry.enabled === true
        };
    }

    async function loadLanguageRegistry() {
        const registry = await fetchJson(
            buildI18nUrl(REGISTRY_FILENAME),
            "Language registry could not be loaded"
        );

        const rawLanguages = Array.isArray(registry.languages)
            ? registry.languages
            : [];

        const normalizedLanguages = rawLanguages
            .map(normalizeLanguageEntry)
            .filter(Boolean);

        enabledLanguages = normalizedLanguages.filter(
            language => language.enabled
        );

        if (!enabledLanguages.length) {
            throw new Error(
                "Language registry does not contain enabled languages."
            );
        }

        const defaultLanguageCode = String(
            registry.defaultLanguage || "en"
        ).toLowerCase();

        const fallbackLanguageCode = String(
            registry.fallbackLanguage || defaultLanguageCode
        ).toLowerCase();

        languageRegistry = {
            version: String(registry.version || "1.0"),
            defaultLanguage: defaultLanguageCode,
            fallbackLanguage: fallbackLanguageCode,
            languages: normalizedLanguages
        };

        return languageRegistry;
    }

    function getLanguageByCode(
        code,
        enabledOnly = true
    ) {
        if (!languageRegistry) {
            return null;
        }

        const languages = enabledOnly
            ? enabledLanguages
            : languageRegistry.languages;

        return languages.find(
            language =>
                language.code ===
                String(code || "").toLowerCase()
        ) || null;
    }

    function getLanguageFromPath() {
        const pathname =
            window.location.pathname.toLowerCase();

        const matchingLanguage =
            [...enabledLanguages]
                .sort(
                    (first, second) =>
                        second.path.length -
                        first.path.length
                )
                .find(language =>
                    pathname.startsWith(
                        language.path.toLowerCase()
                    )
                );

        if (matchingLanguage) {
            return matchingLanguage;
        }

        return (
            getLanguageByCode(
                languageRegistry.defaultLanguage
            ) ||
            enabledLanguages[0]
        );
    }

    function getFallbackLanguage() {
        return (
            getLanguageByCode(
                languageRegistry.fallbackLanguage
            ) ||
            getLanguageByCode(
                languageRegistry.defaultLanguage
            ) ||
            enabledLanguages[0]
        );
    }

    async function loadTranslations(
        languageEntry
    ) {
        return fetchJson(
            buildI18nUrl(
                languageEntry.translationFile
            ),
            "Translation package could not be loaded"
        );
    }

    function setText(
        selector,
        value
    ) {
        if (typeof value !== "string") {
            return;
        }

        const element =
            document.querySelector(selector);

        if (element) {
            element.textContent = value;
        }
    }

    function setTexts(
        selector,
        values
    ) {
        if (!Array.isArray(values)) {
            return;
        }

        const elements =
            document.querySelectorAll(selector);

        elements.forEach(
            (element, index) => {
                if (
                    typeof values[index] === "string"
                ) {
                    element.textContent =
                        values[index];
                }
            }
        );
    }

    function setMetaByName(
        name,
        value
    ) {
        if (typeof value !== "string") {
            return;
        }

        const element = document.querySelector(
            'meta[name="' + name + '"]'
        );

        if (element) {
            element.setAttribute(
                "content",
                value
            );
        }
    }

    function setMetaByProperty(
        property,
        value
    ) {
        if (typeof value !== "string") {
            return;
        }

        const element = document.querySelector(
            'meta[property="' + property + '"]'
        );

        if (element) {
            element.setAttribute(
                "content",
                value
            );
        }
    }
        function setCanonicalUrl(languageEntry) {
        const canonical = document.querySelector(
            'link[rel="canonical"]'
        );

        if (!canonical) {
            return;
        }

        canonical.setAttribute(
            "href",
            new URL(
                languageEntry.path,
                window.location.origin
            ).href
        );
    }

    function rebuildAlternateLanguageLinks() {
        document
            .querySelectorAll(
                'link[rel="alternate"][hreflang]'
            )
            .forEach(link => link.remove());

        enabledLanguages.forEach(language => {
            const link =
                document.createElement("link");

            link.rel = "alternate";
            link.hreflang = language.code;
            link.href = new URL(
                language.path,
                window.location.origin
            ).href;

            document.head.appendChild(link);
        });

        const defaultLanguage =
            getLanguageByCode(
                languageRegistry.defaultLanguage
            ) ||
            enabledLanguages[0];

        if (defaultLanguage) {
            const defaultLink =
                document.createElement("link");

            defaultLink.rel = "alternate";
            defaultLink.hreflang = "x-default";
            defaultLink.href = new URL(
                defaultLanguage.path,
                window.location.origin
            ).href;

            document.head.appendChild(
                defaultLink
            );
        }
    }

    function updateSocialUrls(
        languageEntry
    ) {
        const localizedUrl = new URL(
            languageEntry.path,
            window.location.origin
        ).href;

        setMetaByProperty(
            "og:url",
            localizedUrl
        );
    }

    function getCurrentLocalizedTail() {
        if (!currentLanguageEntry) {
            return "";
        }

        const pathname =
            window.location.pathname;

        const languagePath =
            currentLanguageEntry.path;

        if (
            !pathname
                .toLowerCase()
                .startsWith(
                    languagePath.toLowerCase()
                )
        ) {
            return "";
        }

        return pathname.slice(
            languagePath.length
        );
    }

    function buildLanguageTargetPath(
        languageEntry
    ) {
        const tail =
            getCurrentLocalizedTail();

        const basePath =
            languageEntry.path.endsWith("/")
                ? languageEntry.path
                : languageEntry.path + "/";

        return basePath + tail;
    }

    function updateLocalizedLinks(
        languageEntry
    ) {
        const knownPaths =
            languageRegistry.languages
                .map(
                    language =>
                        language.path
                )
                .sort(
                    (first, second) =>
                        second.length -
                        first.length
                );

        document
            .querySelectorAll("a[href]")
            .forEach(link => {
                const href =
                    link.getAttribute("href");

                if (
                    !href ||
                    href.startsWith("#") ||
                    href.startsWith(
                        "mailto:"
                    ) ||
                    href.startsWith(
                        "tel:"
                    ) ||
                    href.startsWith(
                        "http://"
                    ) ||
                    href.startsWith(
                        "https://"
                    )
                ) {
                    return;
                }

                const matchingPath =
                    knownPaths.find(path =>
                        href
                            .toLowerCase()
                            .startsWith(
                                path.toLowerCase()
                            )
                    );

                if (!matchingPath) {
                    return;
                }

                const remainder =
                    href.slice(
                        matchingPath.length
                    );

                const basePath =
                    languageEntry.path
                        .endsWith("/")
                        ? languageEntry.path
                        : languageEntry.path +
                          "/";

                link.setAttribute(
                    "href",
                    basePath + remainder
                );
            });
    }

    function updateLanguageSelector(
        languageEntry
    ) {
        const select =
            document.getElementById(
                "language-select"
            );

        if (!select) {
            return;
        }

        select.removeAttribute(
            "onchange"
        );

        select.innerHTML = "";

        enabledLanguages.forEach(
            language => {
                const option =
                    document.createElement(
                        "option"
                    );

                option.value =
                    language.code;

                option.textContent =
                    language.nativeName;

                option.selected =
                    language.code ===
                    languageEntry.code;

                select.appendChild(
                    option
                );
            }
        );
    }

    function applyDocumentLanguage(
        languageEntry
    ) {
        document.documentElement.lang =
            languageEntry.code;

        document.documentElement.dir =
            languageEntry.direction;
    }

    function applyTranslations(
        translations,
        languageEntry
    ) {
        if (
            !translations ||
            typeof translations !==
                "object"
        ) {
            return;
        }

        applyDocumentLanguage(
            languageEntry
        );

        if (translations.meta?.title) {
            document.title =
                translations.meta.title;
        }

        setMetaByName(
            "description",
            translations.meta?.description
        );

        setMetaByName(
            "keywords",
            translations.meta?.keywords
        );

        setMetaByProperty(
            "og:locale",
            translations.meta?.locale ||
                languageEntry.locale
        );

        setMetaByProperty(
            "og:title",
            translations.meta?.title
        );

        setMetaByProperty(
            "og:description",
            translations.meta?.description
        );

        setMetaByName(
            "twitter:title",
            translations.meta?.title
        );

        setMetaByName(
            "twitter:description",
            translations.meta?.description
        );

        setText(
            ".skip-link",
            translations.navigation
                ?.skipToContent
        );

        const headerBrand =
            document.querySelector(
                ".site-header .brand"
            );

        const footerBrand =
            document.querySelector(
                ".site-footer .brand"
            );

        const mainNavigation =
            document.querySelector(
                ".main-nav"
            );

        const footerNavigation =
            document.querySelector(
                ".footer-links"
            );

        const languageSelect =
            document.getElementById(
                "language-select"
            );

        if (
            headerBrand &&
            translations.navigation
                ?.homeAriaLabel
        ) {
            headerBrand.setAttribute(
                "aria-label",
                translations.navigation
                    .homeAriaLabel
            );
        }

        if (
            footerBrand &&
            translations.navigation
                ?.homeAriaLabel
        ) {
            footerBrand.setAttribute(
                "aria-label",
                translations.navigation
                    .homeAriaLabel
            );
        }

        if (
            mainNavigation &&
            translations.navigation
                ?.primaryAriaLabel
        ) {
            mainNavigation.setAttribute(
                "aria-label",
                translations.navigation
                    .primaryAriaLabel
            );
        }

        if (
            footerNavigation &&
            translations.navigation
                ?.primaryAriaLabel
        ) {
            footerNavigation.setAttribute(
                "aria-label",
                translations.navigation
                    .primaryAriaLabel
            );
        }

        if (
            languageSelect &&
            translations.navigation
                ?.languageAriaLabel
        ) {
            languageSelect.setAttribute(
                "aria-label",
                translations.navigation
                    .languageAriaLabel
            );
        }
                setTexts(".main-nav a", [
            translations.navigation?.platform,
            translations.navigation?.capabilities,
            translations.navigation?.security,
            translations.navigation?.contact
        ]);

        setText(
            ".hero .eyebrow",
            translations.hero?.eyebrow
        );

        const heroTitle = document.querySelector(
            ".hero h1"
        );

        if (
            heroTitle &&
            translations.hero?.title
        ) {
            heroTitle.textContent =
                translations.hero.title + " ";

            if (translations.hero?.titleAccent) {
                const accent =
                    document.createElement("span");

                accent.className =
                    "gradient-text";

                accent.textContent =
                    translations.hero.titleAccent;

                heroTitle.appendChild(
                    accent
                );
            }
        }

        setText(
            ".hero .lead",
            translations.hero?.description
        );

        setTexts(
            ".hero .hero-actions .button",
            [
                translations.hero?.primaryButton,
                translations.hero?.secondaryButton
            ]
        );

        setTexts(
            ".hero-note span",
            [
                translations.hero?.noteOAuth,
                translations.hero?.noteAuthorized,
                translations.hero?.noteEncrypted
            ]
        );

        setTexts(
            ".preview-label",
            [
                translations.hero
                    ?.previewWorkflowLabel,
                translations.hero
                    ?.previewPublishingLabel,
                translations.hero
                    ?.previewOperationsLabel
            ]
        );

        setTexts(
            ".preview-value",
            [
                translations.hero
                    ?.previewWorkflowValue,
                translations.hero
                    ?.previewPublishingValue
            ]
        );

        setText(
            "#platform .eyebrow",
            translations.platform?.eyebrow
        );

        setText(
            "#platform .section-heading h2",
            translations.platform?.title
        );

        setText(
            "#platform .section-heading .lead",
            translations.platform?.description
        );

        setTexts(
            "#platform .card h3",
            [
                translations.platform
                    ?.creationTitle,
                translations.platform
                    ?.managementTitle,
                translations.platform
                    ?.publishingTitle
            ]
        );

        setTexts(
            "#platform .card .text-muted",
            [
                translations.platform
                    ?.creationText,
                translations.platform
                    ?.managementText,
                translations.platform
                    ?.publishingText
            ]
        );

        setText(
            "#capabilities .eyebrow",
            translations.capabilities
                ?.eyebrow
        );

        setText(
            "#capabilities .section-heading h2",
            translations.capabilities
                ?.title
        );

        setText(
            "#capabilities .section-heading .lead",
            translations.capabilities
                ?.description
        );

        setTexts(
            "#capabilities .card h3",
            [
                translations.capabilities
                    ?.multiPlatformTitle,
                translations.capabilities
                    ?.responsibleTitle
            ]
        );

        setTexts(
            "#capabilities .card > .text-muted",
            [
                translations.capabilities
                    ?.multiPlatformText,
                translations.capabilities
                    ?.responsibleText
            ]
        );

        const capabilityLists =
            document.querySelectorAll(
                "#capabilities .feature-list"
            );

        capabilityLists.forEach(
            (list, listIndex) => {
                const values =
                    listIndex === 0
                        ? translations.capabilities
                            ?.multiPlatformItems
                        : translations.capabilities
                            ?.responsibleItems;

                list
                    .querySelectorAll("li")
                    .forEach(
                        (item, itemIndex) => {
                            if (
                                typeof values?.[
                                    itemIndex
                                ] === "string"
                            ) {
                                item.textContent =
                                    values[itemIndex];
                            }
                        }
                    );
            }
        );

        setText(
            "#security .eyebrow",
            translations.security?.eyebrow
        );

        setText(
            "#security .section-heading h2",
            translations.security?.title
        );

        setText(
            "#security .section-heading .lead",
            translations.security?.description
        );

        document
            .querySelectorAll(
                "#security .trust-item"
            )
            .forEach(
                (item, index) => {
                    const translatedItem =
                        translations.security
                            ?.items?.[index];

                    if (!translatedItem) {
                        return;
                    }

                    const title =
                        item.querySelector(
                            "strong"
                        );

                    const text =
                        item.querySelector(
                            "span"
                        );

                    if (
                        title &&
                        translatedItem.title
                    ) {
                        title.textContent =
                            translatedItem.title;
                    }

                    if (
                        text &&
                        translatedItem.text
                    ) {
                        text.textContent =
                            translatedItem.text;
                    }
                }
            );

        const securityNotice =
            document.querySelector(
                "#security .notice"
            );

        if (securityNotice) {
            securityNotice.textContent = "";

            const label =
                document.createElement(
                    "strong"
                );

            label.textContent =
                translations.security
                    ?.noticeLabel || "";

            securityNotice.appendChild(
                label
            );

            securityNotice.append(
                " " +
                (
                    translations.security
                        ?.noticeText || ""
                )
            );
        }

        setText(
            ".cta-panel .eyebrow",
            translations.policies?.eyebrow
        );

        setText(
            ".cta-panel h2",
            translations.policies?.title
        );

        setText(
            ".cta-panel p",
            translations.policies
                ?.description
        );

        setTexts(
            ".cta-panel .button",
            [
                translations.policies
                    ?.privacyButton,
                translations.policies
                    ?.termsButton
            ]
        );

        setText(
            "#contact .eyebrow",
            translations.contact?.eyebrow
        );

        setText(
            "#contact h2",
            translations.contact?.title
        );

        setText(
            "#contact .lead",
            translations.contact?.description
        );

        setText(
            '#contact a[href^="mailto:"]',
            translations.contact?.email
        );

        setText(
            "#contact > .container > .text-muted",
            translations.contact
                ?.temporaryNotice
        );

        setText(
            ".footer-copy",
            translations.footer?.description
        );

        setTexts(
            ".footer-links a",
            [
                translations.footer?.home,
                translations.footer?.privacy,
                translations.footer?.terms,
                translations.footer?.contact
            ]
        );

        setTexts(
            ".footer-bottom span",
            [
                translations.footer
                    ?.copyright,
                translations.footer
                    ?.rights
            ]
        );

        setCanonicalUrl(
            languageEntry
        );

        rebuildAlternateLanguageLinks();

        updateSocialUrls(
            languageEntry
        );

        updateLocalizedLinks(
            languageEntry
        );

        updateLanguageSelector(
            languageEntry
        );
    }

    async function initLocalization() {
        try {
            await loadLanguageRegistry();

            currentLanguageEntry =
                getLanguageFromPath();

            updateLanguageSelector(
                currentLanguageEntry
            );

            updateLocalizedLinks(
                currentLanguageEntry
            );

            applyDocumentLanguage(
                currentLanguageEntry
            );

            try {
                const translations =
                    await loadTranslations(
                        currentLanguageEntry
                    );

                applyTranslations(
                    translations,
                    currentLanguageEntry
                );

                console.info(
                    "VIS localization loaded:",
                    currentLanguageEntry.code
                );
            } catch (
                translationError
            ) {
                const fallbackLanguage =
                    getFallbackLanguage();

                if (
                    fallbackLanguage &&
                    fallbackLanguage.code !==
                        currentLanguageEntry.code
                ) {
                    const fallbackTranslations =
                        await loadTranslations(
                            fallbackLanguage
                        );

                    applyTranslations(
                        fallbackTranslations,
                        currentLanguageEntry
                    );

                    console.warn(
                        "VIS localization fallback loaded:",
                        fallbackLanguage.code,
                        translationError
                    );
                } else {
                    throw translationError;
                }
            }
        } catch (error) {
            console.warn(
                "VIS localization infrastructure was not loaded. " +
                "The original HTML content remains visible.",
                error
            );
        }
    }
        function initSmoothScroll() {
        document
            .querySelectorAll('a[href^="#"]')
            .forEach(link => {
                link.addEventListener(
                    "click",
                    event => {
                        const href =
                            link.getAttribute("href");

                        if (
                            !href ||
                            href === "#"
                        ) {
                            return;
                        }

                        const target =
                            document.querySelector(href);

                        if (!target) {
                            return;
                        }

                        event.preventDefault();

                        target.scrollIntoView({
                            behavior: "smooth",
                            block: "start"
                        });
                    }
                );
            });
    }

    function initActiveSection() {
        const links =
            document.querySelectorAll(
                '.main-nav a[href*="#"]'
            );

        if (
            !links.length ||
            !("IntersectionObserver" in window)
        ) {
            return;
        }

        const observer =
            new IntersectionObserver(
                entries => {
                    entries.forEach(entry => {
                        if (!entry.isIntersecting) {
                            return;
                        }

                        const id =
                            "#" + entry.target.id;

                        links.forEach(link => {
                            const href =
                                link.getAttribute("href");

                            const active =
                                href &&
                                href.endsWith(id);

                            link.classList.toggle(
                                "active",
                                active
                            );
                        });
                    });
                },
                {
                    threshold: 0.35
                }
            );

        document
            .querySelectorAll("section[id]")
            .forEach(section => {
                observer.observe(section);
            });
    }

    function initRevealAnimation() {
        const elements =
            document.querySelectorAll(
                ".card, section, .legal-content section"
            );

        if (
            !elements.length ||
            !("IntersectionObserver" in window)
        ) {
            return;
        }

        const observer =
            new IntersectionObserver(
                entries => {
                    entries.forEach(entry => {
                        if (!entry.isIntersecting) {
                            return;
                        }

                        entry.target.classList.add(
                            "revealed"
                        );

                        observer.unobserve(
                            entry.target
                        );
                    });
                },
                {
                    threshold: 0.12
                }
            );

        elements.forEach(element => {
            observer.observe(element);
        });
    }

    function initLanguageRemember() {
        const select =
            document.getElementById(
                "language-select"
            );

        if (
            !select ||
            select.dataset
                .visLanguageReady === "true"
        ) {
            return;
        }

        select.dataset.visLanguageReady =
            "true";

        select.addEventListener(
            "change",
            () => {
                const selectedLanguage =
                    getLanguageByCode(
                        select.value
                    );

                if (!selectedLanguage) {
                    return;
                }

                try {
                    localStorage.setItem(
                        "vis-language",
                        selectedLanguage.code
                    );
                } catch (error) {
                    console.warn(
                        "Language preference could not be stored."
                    );
                }

                window.location.href =
                    buildLanguageTargetPath(
                        selectedLanguage
                    );
            }
        );
    }

    async function init() {
        await initLocalization();

        initSmoothScroll();
        initActiveSection();
        initRevealAnimation();
        initLanguageRemember();

        console.info(
            "VIS Website initialized"
        );
    }

    document.addEventListener(
        "DOMContentLoaded",
        init
    );
})();