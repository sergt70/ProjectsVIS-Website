#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

LANGUAGES = [
    "de", "fr", "it", "nl", "es", "ru", "sv", "da",
    "no", "fi", "pt", "pl", "ja", "ko", "zh", "ar",
]

SECTIONS = ("privacy", "terms")

LANGUAGE_LABELS = {
    "de": "Deutsch",
    "fr": "Français",
    "it": "Italiano",
    "nl": "Nederlands",
    "es": "Español",
    "ru": "Русский",
    "sv": "Svenska",
    "da": "Dansk",
    "no": "Norsk",
    "fi": "Suomi",
    "pt": "Português",
    "pl": "Polski",
    "ja": "日本語",
    "ko": "한국어",
    "zh": "简体中文",
    "ar": "العربية",
}

UI = {
    "de": {
        "official": "Offizielle rechtliche Fassung",
        "legal_info": "Rechtliche Informationen",
        "on_page": "Auf dieser Seite",
        "nav_platform": "Plattform",
        "nav_capabilities": "Funktionen",
        "nav_security": "Sicherheit",
        "nav_contact": "Kontakt",
        "footer_home": "Startseite",
        "footer_privacy": "Datenschutzerklärung",
        "footer_terms": "Nutzungsbedingungen",
        "footer_contact": "Rechtlicher Kontakt",
        "footer_copy": "VIS ist eine KI-gestützte Plattform zum Erstellen, Verwalten und Veröffentlichen digitaler Inhalte über autorisierte Social-Media-Verbindungen.",
        "rights": "Alle Rechte vorbehalten.",
        "privacy_nav": [
            "1. Geltungsbereich", "2. Verantwortliche Stelle", "3. Verarbeitete Informationen",
            "4. OAuth-Verbindungen", "5. Verwendung von Informationen", "6. Rechtsgrundlagen",
            "7. Weitergabe und Dienstleister", "8. Speicherung und Sicherheit", "9. Internationale Übermittlungen",
            "10. Aufbewahrung", "11. Ihre Rechte und Wahlmöglichkeiten", "12. Trennung von Konten",
            "13. Cookies und lokale Speicherung", "14. Änderungen", "15. Kontakt",
        ],
        "terms_nav": [
            "1. Zustimmung", "2. Der VIS-Dienst", "3. Berechtigung und Befugnis",
            "4. Verbundene Konten", "5. Nutzerinhalte", "6. Zulässige Nutzung",
            "7. Drittanbieter-Plattformen", "8. Geistiges Eigentum", "9. Verfügbarkeit und Änderungen",
            "10. Haftungsausschlüsse", "11. Haftung", "12. Verantwortung für Ansprüche",
            "13. Sperrung und Beendigung", "14. Datenschutz", "15. Anwendbare Bestimmungen",
            "16. Änderungen", "17. Kontakt",
        ],
    },
    "fr": {
        "official": "Version juridique officielle",
        "legal_info": "Informations juridiques",
        "on_page": "Sur cette page",
        "nav_platform": "Plateforme",
        "nav_capabilities": "Fonctionnalités",
        "nav_security": "Sécurité",
        "nav_contact": "Contact",
        "footer_home": "Accueil",
        "footer_privacy": "Politique de confidentialité",
        "footer_terms": "Conditions d’utilisation",
        "footer_contact": "Contact juridique",
        "footer_copy": "VIS est une plateforme alimentée par l’IA pour créer, gérer et publier du contenu numérique via des connexions autorisées aux réseaux sociaux.",
        "rights": "Tous droits réservés.",
        "privacy_nav": [
            "1. Champ d’application", "2. Responsable", "3. Informations traitées",
            "4. Connexions OAuth", "5. Utilisation des informations", "6. Bases juridiques",
            "7. Partage et prestataires", "8. Stockage et sécurité", "9. Transferts internationaux",
            "10. Conservation", "11. Vos droits et choix", "12. Déconnexion des comptes",
            "13. Cookies et stockage local", "14. Modifications", "15. Contact",
        ],
        "terms_nav": [
            "1. Acceptation", "2. Service VIS", "3. Éligibilité et autorité",
            "4. Comptes connectés", "5. Contenu utilisateur", "6. Utilisation acceptable",
            "7. Plateformes tierces", "8. Propriété intellectuelle", "9. Disponibilité et modifications",
            "10. Exclusions de garantie", "11. Responsabilité", "12. Responsabilité pour les réclamations",
            "13. Suspension et résiliation", "14. Confidentialité", "15. Dispositions applicables",
            "16. Modifications", "17. Contact",
        ],
    },
    "it": {
        "official": "Versione legale ufficiale",
        "legal_info": "Informazioni legali",
        "on_page": "In questa pagina",
        "nav_platform": "Piattaforma",
        "nav_capabilities": "Funzionalità",
        "nav_security": "Sicurezza",
        "nav_contact": "Contatti",
        "footer_home": "Home",
        "footer_privacy": "Informativa sulla privacy",
        "footer_terms": "Termini di servizio",
        "footer_contact": "Contatto legale",
        "footer_copy": "VIS è una piattaforma basata sull’IA per creare, gestire e pubblicare contenuti digitali tramite connessioni autorizzate ai social media.",
        "rights": "Tutti i diritti riservati.",
        "privacy_nav": [
            "1. Ambito", "2. Titolare responsabile", "3. Informazioni trattate",
            "4. Connessioni OAuth", "5. Uso delle informazioni", "6. Basi giuridiche",
            "7. Condivisione e fornitori", "8. Archiviazione e sicurezza", "9. Trasferimenti internazionali",
            "10. Conservazione", "11. Diritti e scelte", "12. Disconnessione degli account",
            "13. Cookie e archiviazione locale", "14. Modifiche", "15. Contatti",
        ],
        "terms_nav": [
            "1. Accettazione", "2. Servizio VIS", "3. Idoneità e autorità",
            "4. Account collegati", "5. Contenuti dell’utente", "6. Uso accettabile",
            "7. Piattaforme di terze parti", "8. Proprietà intellettuale", "9. Disponibilità e modifiche",
            "10. Esclusioni di garanzia", "11. Responsabilità", "12. Responsabilità per reclami",
            "13. Sospensione e cessazione", "14. Privacy", "15. Condizioni applicabili",
            "16. Modifiche", "17. Contatti",
        ],
    },
    "nl": {
        "official": "Officiële juridische versie",
        "legal_info": "Juridische informatie",
        "on_page": "Op deze pagina",
        "nav_platform": "Platform",
        "nav_capabilities": "Mogelijkheden",
        "nav_security": "Beveiliging",
        "nav_contact": "Contact",
        "footer_home": "Home",
        "footer_privacy": "Privacybeleid",
        "footer_terms": "Servicevoorwaarden",
        "footer_contact": "Juridisch contact",
        "footer_copy": "VIS is een AI-platform voor het maken, beheren en publiceren van digitale content via geautoriseerde socialemediaverbindingen.",
        "rights": "Alle rechten voorbehouden.",
        "privacy_nav": [
            "1. Toepassingsgebied", "2. Verantwoordelijke", "3. Verwerkte informatie",
            "4. OAuth-verbindingen", "5. Gebruik van informatie", "6. Rechtsgronden",
            "7. Delen en dienstverleners", "8. Opslag en beveiliging", "9. Internationale overdrachten",
            "10. Bewaartermijnen", "11. Uw rechten en keuzes", "12. Accounts loskoppelen",
            "13. Cookies en lokale opslag", "14. Wijzigingen", "15. Contact",
        ],
        "terms_nav": [
            "1. Aanvaarding", "2. De VIS-dienst", "3. Geschiktheid en bevoegdheid",
            "4. Verbonden accounts", "5. Gebruikersinhoud", "6. Toegestaan gebruik",
            "7. Platforms van derden", "8. Intellectueel eigendom", "9. Beschikbaarheid en wijzigingen",
            "10. Disclaimers", "11. Aansprakelijkheid", "12. Verantwoordelijkheid voor claims",
            "13. Opschorting en beëindiging", "14. Privacy", "15. Toepasselijke bepalingen",
            "16. Wijzigingen", "17. Contact",
        ],
    },
    "es": {
        "official": "Versión jurídica oficial",
        "legal_info": "Información legal",
        "on_page": "En esta página",
        "nav_platform": "Plataforma",
        "nav_capabilities": "Funciones",
        "nav_security": "Seguridad",
        "nav_contact": "Contacto",
        "footer_home": "Inicio",
        "footer_privacy": "Política de privacidad",
        "footer_terms": "Términos del servicio",
        "footer_contact": "Contacto legal",
        "footer_copy": "VIS es una plataforma impulsada por IA para crear, gestionar y publicar contenido digital mediante conexiones autorizadas a redes sociales.",
        "rights": "Todos los derechos reservados.",
        "privacy_nav": [
            "1. Alcance", "2. Responsable", "3. Información que procesamos",
            "4. Conexiones OAuth", "5. Uso de la información", "6. Bases legales",
            "7. Compartición y proveedores", "8. Almacenamiento y seguridad", "9. Transferencias internacionales",
            "10. Conservación", "11. Sus derechos y opciones", "12. Desconexión de cuentas",
            "13. Cookies y almacenamiento local", "14. Cambios", "15. Contacto",
        ],
        "terms_nav": [
            "1. Aceptación", "2. El servicio VIS", "3. Elegibilidad y autoridad",
            "4. Cuentas conectadas", "5. Contenido del usuario", "6. Uso aceptable",
            "7. Plataformas de terceros", "8. Propiedad intelectual", "9. Disponibilidad y cambios",
            "10. Exenciones de responsabilidad", "11. Responsabilidad", "12. Responsabilidad por reclamaciones",
            "13. Suspensión y terminación", "14. Privacidad", "15. Términos aplicables",
            "16. Cambios", "17. Contacto",
        ],
    },
    "ru": {
        "official": "Официальная юридическая версия",
        "legal_info": "Юридическая информация",
        "on_page": "На этой странице",
        "nav_platform": "Платформа",
        "nav_capabilities": "Возможности",
        "nav_security": "Безопасность",
        "nav_contact": "Контакты",
        "footer_home": "Главная",
        "footer_privacy": "Политика конфиденциальности",
        "footer_terms": "Условия использования",
        "footer_contact": "Юридический контакт",
        "footer_copy": "VIS — платформа на базе искусственного интеллекта для создания, управления и публикации цифрового контента через авторизованные подключения к социальным сетям.",
        "rights": "Все права защищены.",
        "privacy_nav": [
            "1. Область действия", "2. Ответственная сторона", "3. Обрабатываемая информация",
            "4. Подключения OAuth", "5. Использование информации", "6. Правовые основания",
            "7. Передача данных и поставщики услуг", "8. Хранение и безопасность", "9. Международная передача данных",
            "10. Сроки хранения", "11. Ваши права и выбор", "12. Отключение аккаунтов",
            "13. Файлы cookie и локальное хранилище", "14. Изменения", "15. Контакты",
        ],
        "terms_nav": [
            "1. Принятие условий", "2. Сервис VIS", "3. Право использования и полномочия",
            "4. Подключённые аккаунты", "5. Пользовательский контент", "6. Допустимое использование",
            "7. Сторонние платформы", "8. Интеллектуальная собственность", "9. Доступность и изменения",
            "10. Отказ от гарантий", "11. Ответственность", "12. Ответственность по претензиям",
            "13. Приостановка и прекращение", "14. Конфиденциальность", "15. Применимые положения",
            "16. Изменения", "17. Контакты",
        ],
    },
    "sv": {
        "official": "Officiell juridisk version",
        "legal_info": "Juridisk information",
        "on_page": "På den här sidan",
        "nav_platform": "Plattform",
        "nav_capabilities": "Funktioner",
        "nav_security": "Säkerhet",
        "nav_contact": "Kontakt",
        "footer_home": "Hem",
        "footer_privacy": "Integritetspolicy",
        "footer_terms": "Användarvillkor",
        "footer_contact": "Juridisk kontakt",
        "footer_copy": "VIS är en AI-driven plattform för att skapa, hantera och publicera digitalt innehåll via auktoriserade anslutningar till sociala medier.",
        "rights": "Alla rättigheter förbehållna.",
        "privacy_nav": [
            "1. Omfattning", "2. Ansvarig part", "3. Information vi behandlar",
            "4. OAuth-anslutningar", "5. Hur information används", "6. Rättsliga grunder",
            "7. Delning och tjänsteleverantörer", "8. Lagring och säkerhet", "9. Internationella överföringar",
            "10. Lagringstid", "11. Dina rättigheter och val", "12. Frånkoppling av konton",
            "13. Cookies och lokal lagring", "14. Ändringar", "15. Kontakt",
        ],
        "terms_nav": [
            "1. Godkännande", "2. VIS-tjänsten", "3. Behörighet och befogenhet",
            "4. Anslutna konton", "5. Användarinnehåll", "6. Tillåten användning",
            "7. Tredjepartsplattformar", "8. Immateriella rättigheter", "9. Tillgänglighet och ändringar",
            "10. Ansvarsfriskrivningar", "11. Ansvar", "12. Ansvar för krav",
            "13. Avstängning och uppsägning", "14. Integritet", "15. Tillämpliga villkor",
            "16. Ändringar", "17. Kontakt",
        ],
    },
    "da": {
        "official": "Officiel juridisk version",
        "legal_info": "Juridiske oplysninger",
        "on_page": "På denne side",
        "nav_platform": "Platform",
        "nav_capabilities": "Funktioner",
        "nav_security": "Sikkerhed",
        "nav_contact": "Kontakt",
        "footer_home": "Hjem",
        "footer_privacy": "Privatlivspolitik",
        "footer_terms": "Servicevilkår",
        "footer_contact": "Juridisk kontakt",
        "footer_copy": "VIS er en AI-drevet platform til at oprette, administrere og udgive digitalt indhold via autoriserede forbindelser til sociale medier.",
        "rights": "Alle rettigheder forbeholdes.",
        "privacy_nav": [
            "1. Omfang", "2. Ansvarlig part", "3. Oplysninger vi behandler",
            "4. OAuth-forbindelser", "5. Brug af oplysninger", "6. Retsgrundlag",
            "7. Deling og tjenesteudbydere", "8. Opbevaring og sikkerhed", "9. Internationale overførsler",
            "10. Opbevaringsperiode", "11. Dine rettigheder og valg", "12. Frakobling af konti",
            "13. Cookies og lokal lagring", "14. Ændringer", "15. Kontakt",
        ],
        "terms_nav": [
            "1. Accept", "2. VIS-tjenesten", "3. Berettigelse og bemyndigelse",
            "4. Tilknyttede konti", "5. Brugerindhold", "6. Acceptabel brug",
            "7. Tredjepartsplatforme", "8. Immaterielle rettigheder", "9. Tilgængelighed og ændringer",
            "10. Ansvarsfraskrivelser", "11. Ansvar", "12. Ansvar for krav",
            "13. Suspension og ophør", "14. Privatliv", "15. Gældende vilkår",
            "16. Ændringer", "17. Kontakt",
        ],
    },
    "no": {
        "official": "Offisiell juridisk versjon",
        "legal_info": "Juridisk informasjon",
        "on_page": "På denne siden",
        "nav_platform": "Plattform",
        "nav_capabilities": "Funksjoner",
        "nav_security": "Sikkerhet",
        "nav_contact": "Kontakt",
        "footer_home": "Hjem",
        "footer_privacy": "Personvernerklæring",
        "footer_terms": "Tjenestevilkår",
        "footer_contact": "Juridisk kontakt",
        "footer_copy": "VIS er en KI-drevet plattform for å opprette, administrere og publisere digitalt innhold via autoriserte tilkoblinger til sosiale medier.",
        "rights": "Alle rettigheter forbeholdt.",
        "privacy_nav": [
            "1. Omfang", "2. Ansvarlig part", "3. Informasjon vi behandler",
            "4. OAuth-tilkoblinger", "5. Bruk av informasjon", "6. Rettslig grunnlag",
            "7. Deling og tjenesteleverandører", "8. Lagring og sikkerhet", "9. Internasjonale overføringer",
            "10. Oppbevaring", "11. Dine rettigheter og valg", "12. Frakobling av kontoer",
            "13. Informasjonskapsler og lokal lagring", "14. Endringer", "15. Kontakt",
        ],
        "terms_nav": [
            "1. Aksept", "2. VIS-tjenesten", "3. Kvalifikasjon og myndighet",
            "4. Tilknyttede kontoer", "5. Brukerinnhold", "6. Akseptabel bruk",
            "7. Tredjepartsplattformer", "8. Immaterielle rettigheter", "9. Tilgjengelighet og endringer",
            "10. Ansvarsfraskrivelser", "11. Ansvar", "12. Ansvar for krav",
            "13. Suspensjon og avslutning", "14. Personvern", "15. Gjeldende vilkår",
            "16. Endringer", "17. Kontakt",
        ],
    },
    "fi": {
        "official": "Virallinen oikeudellinen versio",
        "legal_info": "Oikeudelliset tiedot",
        "on_page": "Tällä sivulla",
        "nav_platform": "Alusta",
        "nav_capabilities": "Ominaisuudet",
        "nav_security": "Turvallisuus",
        "nav_contact": "Yhteystiedot",
        "footer_home": "Etusivu",
        "footer_privacy": "Tietosuojakäytäntö",
        "footer_terms": "Käyttöehdot",
        "footer_contact": "Oikeudellinen yhteydenotto",
        "footer_copy": "VIS on tekoälypohjainen alusta digitaalisen sisällön luomiseen, hallintaan ja julkaisemiseen valtuutettujen sosiaalisen median yhteyksien kautta.",
        "rights": "Kaikki oikeudet pidätetään.",
        "privacy_nav": [
            "1. Soveltamisala", "2. Rekisterinpitäjä", "3. Käsittelemämme tiedot",
            "4. OAuth-yhteydet", "5. Tietojen käyttö", "6. Oikeusperusteet",
            "7. Tietojen jakaminen ja palveluntarjoajat", "8. Säilytys ja turvallisuus", "9. Kansainväliset siirrot",
            "10. Säilytysajat", "11. Oikeutesi ja valintasi", "12. Tilien irrottaminen",
            "13. Evästeet ja paikallinen tallennus", "14. Muutokset", "15. Yhteystiedot",
        ],
        "terms_nav": [
            "1. Hyväksyminen", "2. VIS-palvelu", "3. Kelpoisuus ja valtuudet",
            "4. Yhdistetyt tilit", "5. Käyttäjäsisältö", "6. Hyväksyttävä käyttö",
            "7. Kolmannen osapuolen alustat", "8. Immateriaalioikeudet", "9. Saatavuus ja muutokset",
            "10. Vastuuvapauslausekkeet", "11. Vastuu", "12. Vastuu vaatimuksista",
            "13. Keskeyttäminen ja päättäminen", "14. Tietosuoja", "15. Sovellettavat ehdot",
            "16. Muutokset", "17. Yhteystiedot",
        ],
    },
    "pt": {
        "official": "Versão jurídica oficial",
        "legal_info": "Informações jurídicas",
        "on_page": "Nesta página",
        "nav_platform": "Plataforma",
        "nav_capabilities": "Funcionalidades",
        "nav_security": "Segurança",
        "nav_contact": "Contato",
        "footer_home": "Início",
        "footer_privacy": "Política de Privacidade",
        "footer_terms": "Termos de Serviço",
        "footer_contact": "Contato jurídico",
        "footer_copy": "A VIS é uma plataforma com IA para criar, gerir e publicar conteúdo digital por meio de conexões autorizadas com redes sociais.",
        "rights": "Todos os direitos reservados.",
        "privacy_nav": [
            "1. Âmbito", "2. Responsável", "3. Informações que tratamos",
            "4. Conexões OAuth", "5. Utilização das informações", "6. Bases legais",
            "7. Partilha e prestadores de serviços", "8. Armazenamento e segurança", "9. Transferências internacionais",
            "10. Retenção", "11. Seus direitos e escolhas", "12. Desconexão de contas",
            "13. Cookies e armazenamento local", "14. Alterações", "15. Contato",
        ],
        "terms_nav": [
            "1. Aceitação", "2. Serviço VIS", "3. Elegibilidade e autoridade",
            "4. Contas conectadas", "5. Conteúdo do utilizador", "6. Utilização aceitável",
            "7. Plataformas de terceiros", "8. Propriedade intelectual", "9. Disponibilidade e alterações",
            "10. Isenções de responsabilidade", "11. Responsabilidade", "12. Responsabilidade por reclamações",
            "13. Suspensão e encerramento", "14. Privacidade", "15. Termos aplicáveis",
            "16. Alterações", "17. Contato",
        ],
    },
    "pl": {
        "official": "Oficjalna wersja prawna",
        "legal_info": "Informacje prawne",
        "on_page": "Na tej stronie",
        "nav_platform": "Platforma",
        "nav_capabilities": "Możliwości",
        "nav_security": "Bezpieczeństwo",
        "nav_contact": "Kontakt",
        "footer_home": "Strona główna",
        "footer_privacy": "Polityka prywatności",
        "footer_terms": "Warunki korzystania",
        "footer_contact": "Kontakt prawny",
        "footer_copy": "VIS to platforma oparta na AI do tworzenia, zarządzania i publikowania treści cyfrowych za pośrednictwem autoryzowanych połączeń z mediami społecznościowymi.",
        "rights": "Wszelkie prawa zastrzeżone.",
        "privacy_nav": [
            "1. Zakres", "2. Podmiot odpowiedzialny", "3. Przetwarzane informacje",
            "4. Połączenia OAuth", "5. Wykorzystanie informacji", "6. Podstawy prawne",
            "7. Udostępnianie i usługodawcy", "8. Przechowywanie i bezpieczeństwo", "9. Transfery międzynarodowe",
            "10. Okres przechowywania", "11. Twoje prawa i wybory", "12. Odłączanie kont",
            "13. Pliki cookie i pamięć lokalna", "14. Zmiany", "15. Kontakt",
        ],
        "terms_nav": [
            "1. Akceptacja", "2. Usługa VIS", "3. Uprawnienia i umocowanie",
            "4. Połączone konta", "5. Treści użytkownika", "6. Dozwolone użycie",
            "7. Platformy zewnętrzne", "8. Własność intelektualna", "9. Dostępność i zmiany",
            "10. Wyłączenia odpowiedzialności", "11. Odpowiedzialność", "12. Odpowiedzialność za roszczenia",
            "13. Zawieszenie i zakończenie", "14. Prywatność", "15. Obowiązujące warunki",
            "16. Zmiany", "17. Kontakt",
        ],
    },
    "ja": {
        "official": "公式の法的文書",
        "legal_info": "法的情報",
        "on_page": "このページの内容",
        "nav_platform": "プラットフォーム",
        "nav_capabilities": "機能",
        "nav_security": "セキュリティ",
        "nav_contact": "お問い合わせ",
        "footer_home": "ホーム",
        "footer_privacy": "プライバシーポリシー",
        "footer_terms": "利用規約",
        "footer_contact": "法務窓口",
        "footer_copy": "VISは、認可されたソーシャルメディア接続を通じてデジタルコンテンツを作成・管理・公開するためのAIプラットフォームです。",
        "rights": "無断転載を禁じます。",
        "privacy_nav": [
            "1. 適用範囲", "2. 責任主体", "3. 処理する情報", "4. OAuth接続",
            "5. 情報の利用", "6. 法的根拠", "7. 共有とサービス提供者", "8. 保存とセキュリティ",
            "9. 国際移転", "10. 保存期間", "11. 利用者の権利と選択", "12. アカウントの切断",
            "13. Cookieとローカル保存", "14. 変更", "15. お問い合わせ",
        ],
        "terms_nav": [
            "1. 規約への同意", "2. VISサービス", "3. 利用資格と権限", "4. 接続済みアカウント",
            "5. ユーザーコンテンツ", "6. 許容される利用", "7. 第三者プラットフォーム", "8. 知的財産",
            "9. 提供状況と変更", "10. 免責事項", "11. 責任", "12. 請求に対する責任",
            "13. 停止と終了", "14. プライバシー", "15. 適用条件", "16. 変更", "17. お問い合わせ",
        ],
    },
    "ko": {
        "official": "공식 법적 버전",
        "legal_info": "법적 정보",
        "on_page": "이 페이지의 내용",
        "nav_platform": "플랫폼",
        "nav_capabilities": "기능",
        "nav_security": "보안",
        "nav_contact": "문의",
        "footer_home": "홈",
        "footer_privacy": "개인정보 처리방침",
        "footer_terms": "서비스 이용약관",
        "footer_contact": "법무 문의",
        "footer_copy": "VIS는 승인된 소셜 미디어 연결을 통해 디지털 콘텐츠를 제작, 관리 및 게시할 수 있도록 지원하는 AI 기반 플랫폼입니다.",
        "rights": "모든 권리 보유.",
        "privacy_nav": [
            "1. 적용 범위", "2. 책임 주체", "3. 처리하는 정보", "4. OAuth 연결",
            "5. 정보 사용", "6. 법적 근거", "7. 공유 및 서비스 제공업체", "8. 저장 및 보안",
            "9. 국제 이전", "10. 보유 기간", "11. 이용자의 권리와 선택", "12. 계정 연결 해제",
            "13. 쿠키 및 로컬 저장소", "14. 변경", "15. 문의",
        ],
        "terms_nav": [
            "1. 약관 동의", "2. VIS 서비스", "3. 자격 및 권한", "4. 연결된 계정",
            "5. 사용자 콘텐츠", "6. 허용되는 사용", "7. 제3자 플랫폼", "8. 지식재산권",
            "9. 가용성 및 변경", "10. 면책", "11. 책임", "12. 청구에 대한 책임",
            "13. 정지 및 종료", "14. 개인정보 보호", "15. 적용 조건", "16. 변경", "17. 문의",
        ],
    },
    "zh": {
        "official": "官方法律版本",
        "legal_info": "法律信息",
        "on_page": "本页内容",
        "nav_platform": "平台",
        "nav_capabilities": "功能",
        "nav_security": "安全",
        "nav_contact": "联系",
        "footer_home": "首页",
        "footer_privacy": "隐私政策",
        "footer_terms": "服务条款",
        "footer_contact": "法律联系",
        "footer_copy": "VIS 是一个由人工智能驱动的平台，可通过经授权的社交媒体连接创建、管理和发布数字内容。",
        "rights": "保留所有权利。",
        "privacy_nav": [
            "1. 适用范围", "2. 责任主体", "3. 我们处理的信息", "4. OAuth 连接",
            "5. 信息的使用", "6. 法律依据", "7. 共享与服务提供商", "8. 存储与安全",
            "9. 国际传输", "10. 保留期限", "11. 您的权利与选择", "12. 断开账户连接",
            "13. Cookie 与本地存储", "14. 变更", "15. 联系方式",
        ],
        "terms_nav": [
            "1. 接受条款", "2. VIS 服务", "3. 资格与授权", "4. 已连接账户",
            "5. 用户内容", "6. 可接受的使用", "7. 第三方平台", "8. 知识产权",
            "9. 可用性与变更", "10. 免责声明", "11. 责任", "12. 索赔责任",
            "13. 暂停与终止", "14. 隐私", "15. 适用条款", "16. 变更", "17. 联系方式",
        ],
    },
    "ar": {
        "official": "النسخة القانونية الرسمية",
        "legal_info": "معلومات قانونية",
        "on_page": "في هذه الصفحة",
        "nav_platform": "المنصة",
        "nav_capabilities": "الإمكانات",
        "nav_security": "الأمان",
        "nav_contact": "اتصل بنا",
        "footer_home": "الرئيسية",
        "footer_privacy": "سياسة الخصوصية",
        "footer_terms": "شروط الخدمة",
        "footer_contact": "التواصل القانوني",
        "footer_copy": "VIS منصة مدعومة بالذكاء الاصطناعي لإنشاء المحتوى الرقمي وإدارته ونشره عبر اتصالات مصرح بها مع منصات التواصل الاجتماعي.",
        "rights": "جميع الحقوق محفوظة.",
        "privacy_nav": [
            "1. النطاق", "2. الجهة المسؤولة", "3. المعلومات التي نعالجها", "4. اتصالات OAuth",
            "5. كيفية استخدام المعلومات", "6. الأسس القانونية", "7. المشاركة ومقدمو الخدمات",
            "8. التخزين والأمان", "9. عمليات النقل الدولية", "10. الاحتفاظ",
            "11. حقوقك وخياراتك", "12. فصل الحسابات", "13. ملفات تعريف الارتباط والتخزين المحلي",
            "14. التغييرات", "15. التواصل",
        ],
        "terms_nav": [
            "1. قبول الشروط", "2. خدمة VIS", "3. الأهلية والصلاحية", "4. الحسابات المتصلة",
            "5. محتوى المستخدم", "6. الاستخدام المقبول", "7. منصات الجهات الخارجية",
            "8. الملكية الفكرية", "9. التوفر والتغييرات", "10. إخلاء المسؤولية",
            "11. المسؤولية", "12. المسؤولية عن المطالبات", "13. التعليق والإنهاء",
            "14. الخصوصية", "15. الشروط المطبقة", "16. التغييرات", "17. التواصل",
        ],
    },
}


def replace_legal_nav(text: str, labels: list[str]) -> str:
    block_match = re.search(
        r'(<aside class="legal-nav"[^>]*>\s*<strong>)(.*?)(</strong>)(.*?)(</aside>)',
        text,
        flags=re.S,
    )
    if not block_match:
        raise RuntimeError("Legal navigation block was not found.")

    block = block_match.group(0)
    links = re.findall(r'(<a href="#[^"]+">)(.*?)(</a>)', block, flags=re.S)
    if len(links) != len(labels):
        raise RuntimeError(
            f"Legal navigation item count mismatch: expected {len(labels)}, found {len(links)}."
        )

    translated = block
    for (open_tag, old_label, close_tag), new_label in zip(links, labels):
        translated = translated.replace(
            open_tag + old_label + close_tag,
            open_tag + new_label + close_tag,
            1,
        )

    return text.replace(block, translated, 1)


def localize_footer(text: str, lang: str) -> str:
    ui = UI[lang]

    text = text.replace(
        '<a href="/en/">Home</a>',
        f'<a href="/{lang}/">{ui["footer_home"]}</a>',
        1,
    )
    text = text.replace(
        '<a href="/en/privacy/">Privacy Policy</a>',
        f'<a href="/{lang}/privacy/">{ui["footer_privacy"]}</a>',
        1,
    )
    text = text.replace(
        '<a href="/en/terms/" aria-current="page">Terms of Service</a>',
        f'<a href="/{lang}/terms/" aria-current="page">{ui["footer_terms"]}</a>',
        1,
    )
    text = text.replace(
        '<a href="/en/privacy/" aria-current="page">Privacy Policy</a>',
        f'<a href="/{lang}/privacy/" aria-current="page">{ui["footer_privacy"]}</a>',
        1,
    )
    text = text.replace(
        '<a href="/en/terms/">Terms of Service</a>',
        f'<a href="/{lang}/terms/">{ui["footer_terms"]}</a>',
        1,
    )
    text = text.replace(
        '<a href="mailto:legal@visautomation.com">Legal Contact</a>',
        f'<a href="mailto:legal@visautomation.com">{ui["footer_contact"]}</a>',
        1,
    )
    text = text.replace(
        '<a href="mailto:privacy@visautomation.com">Privacy Contact</a>',
        f'<a href="mailto:privacy@visautomation.com">{ui["footer_contact"]}</a>',
        1,
    )

    english_footer_copy = (
        "VIS is an AI-powered platform for creating, managing and publishing\n"
        "                            digital content through authorized social media connections."
    )
    localized_footer_copy = ui["footer_copy"]
    text = text.replace(english_footer_copy, localized_footer_copy, 1)

    text = text.replace(
        "<span>All rights reserved.</span>",
        f'<span>{ui["rights"]}</span>',
        1,
    )
    return text


def main() -> int:
    root = Path(__file__).resolve().parent
    templates = {
        "privacy": root / "en" / "privacy" / "index.html",
        "terms": root / "en" / "terms" / "index.html",
    }

    missing = [
        str(path.relative_to(root))
        for path in templates.values()
        if not path.is_file()
    ]
    if missing:
        print("ERROR: Missing English legal templates:")
        for item in missing:
            print(f"  - {item}")
        return 1

    expected_logo = (
        "../../assets/images/BrandGraphics/"
        "VIS_Brand_Graphics_v1.0/06_Logo_SVG/"
        "VIS-Logo-Horizontal-Dark.svg"
    )
    for section, path in templates.items():
        content = path.read_text(encoding="utf-8")
        if expected_logo not in content:
            print(f"ERROR: en/{section}/index.html does not contain the current VIS logo path.")
            return 1

    print("English legal templates validated.")
    print()

    written = []

    for lang in LANGUAGES:
        ui = UI[lang]

        for section in SECTIONS:
            source = templates[section]
            target = root / lang / section / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)

            text = source.read_text(encoding="utf-8")

            text = text.replace(
                '<html lang="en">',
                f'<html lang="{lang}"' + (' dir="rtl">' if lang == "ar" else ">"),
                1,
            )

            text = text.replace(
                f'<option value="/en/{section}/" selected>English</option>',
                f'<option value="/en/{section}/">English</option>',
                1,
            )
            label = LANGUAGE_LABELS[lang]
            text = text.replace(
                f'<option value="/{lang}/{section}/">{label}</option>',
                f'<option value="/{lang}/{section}/" selected>{label}</option>',
                1,
            )

            text = text.replace(
                f"https://example.com/en/{section}/",
                f"https://example.com/{lang}/{section}/",
            )

            for code in ["en", "de", "fr", "it", "nl", "es", "ru", "sv",
                         "da", "no", "fi", "pt", "pl", "ja", "ko", "zh", "ar"]:
                text = text.replace(
                    f'hreflang="{code}" href="https://example.com/{lang}/{section}/"',
                    f'hreflang="{code}" href="https://example.com/{code}/{section}/"',
                )

            text = text.replace(
                f'hreflang="x-default" href="https://example.com/{lang}/{section}/"',
                f'hreflang="x-default" href="https://example.com/en/{section}/"',
            )

            # Localize top navigation routes AND visible labels.
            text = text.replace(
                '<a href="/en/#platform">Platform</a>',
                f'<a href="/{lang}/#platform">{ui["nav_platform"]}</a>',
                1,
            )
            text = text.replace(
                '<a href="/en/#capabilities">Capabilities</a>',
                f'<a href="/{lang}/#capabilities">{ui["nav_capabilities"]}</a>',
                1,
            )
            text = text.replace(
                '<a href="/en/#security">Security</a>',
                f'<a href="/{lang}/#security">{ui["nav_security"]}</a>',
                1,
            )
            text = text.replace(
                '<a href="/en/#contact">Contact</a>',
                f'<a href="/{lang}/#contact">{ui["nav_contact"]}</a>',
                1,
            )
            text = text.replace('href="/en/"', f'href="/{lang}/"')

            # Localize only the legal-page interface, never the legal document body.
            text = text.replace(
                '<span class="eyebrow">Legal information</span>',
                f'<span class="eyebrow">{ui["legal_info"]}</span>',
                1,
            )

            text = text.replace(
                '<strong>On this page</strong>',
                f'<strong>{ui["on_page"]}</strong>',
                1,
            )

            labels = ui["privacy_nav"] if section == "privacy" else ui["terms_nav"]
            text = replace_legal_nav(text, labels)

            # Replace the generated notice from the English template.
            notice = (
                '\n            <div class="container" style="padding-top: 20px;">\n'
                '                <div class="notice">\n'
                f'                    <strong>{ui["official"]}:</strong> English.\n'
                '                </div>\n'
                '            </div>\n'
            )
            text = text.replace(
                '        <main id="main-content">\n',
                '        <main id="main-content">\n' + notice,
                1,
            )

            # Footer UI is localized; legal body remains English.
            text = localize_footer(text, lang)

            # Final route replacements after footer localization.
            text = text.replace('href="/en/privacy/"', f'href="/{lang}/privacy/"')
            text = text.replace('href="/en/terms/"', f'href="/{lang}/terms/"')

            if lang == "ar":
                text = text.replace(
                    '<a href="mailto:legal@visautomation.com">',
                    '<a href="mailto:legal@visautomation.com" dir="ltr">',
                )
                text = text.replace(
                    '<a href="mailto:privacy@visautomation.com">',
                    '<a href="mailto:privacy@visautomation.com" dir="ltr">',
                )

            target.write_text(text, encoding="utf-8")
            written.append(str(target.relative_to(root)))

    print(f"Generated {len(written)} legal route pages:")
    for item in written:
        print(f"  OK  {item}")

    print()
    print("UI localization applied:")
    print("  - top navigation labels and routes")
    print("  - legal-page eyebrow")
    print("  - official English-version notice")
    print("  - sidebar title and section bookmarks")
    print("  - footer links, description and rights text")
    print()
    print("Legal document body remains English on every language route.")
    print("Generation completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
