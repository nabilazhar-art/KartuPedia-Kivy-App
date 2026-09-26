"""Utilitas kecil untuk memanggil coroutine (method async pada AppShell, dsb)
dari handler on_click/on_tap Flet, termasuk saat perlu menyisipkan argumen
per-item di dalam list comprehension (mis. game id).

Kenapa perlu ini: `on_click=lambda e: some_async_method()` TIDAK benar-benar
menjalankan coroutine-nya (cuma membuat objek coroutine yang tidak pernah
di-await) -- bug diam-diam, tombol terlihat normal tapi tidak melakukan
apa-apa. Bungkus lewat async_handler() supaya coroutine-nya benar-benar
dijalankan (di-await) saat tombol ditekan.
"""


def async_handler(coro_func, *args, **kwargs):
    """coro_func harus berupa method/fungsi async. args/kwargs diikat SAAT
    async_handler() dipanggil (bukan saat tombol ditekan), jadi aman dipakai
    langsung di dalam list comprehension tanpa trik default-argument."""

    async def handler(e=None):
        await coro_func(*args, **kwargs)

    return handler
