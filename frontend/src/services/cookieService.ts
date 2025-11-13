export function useCookieService() {
    function setCookie(name: string, value: string, days?: number) {
        let maxAge = '';
        if (days) {
            maxAge = `; max-age=${days * 24 * 60 * 60}`;
        }
        document.cookie = `${name}=${value}; path=/${maxAge}`;
    };

    function getCookie(name: string): string | undefined {
        const sections = document.cookie.split('; ');
        for (const section of sections) {
            const [cookieName, cookieValue] = section.split('=');
            if (cookieName === name) {
                return cookieValue;
            }
        }
        return undefined;
    }

    return { setCookie, getCookie }
};