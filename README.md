## Smoke effect in pygame by Rounak Bhowmik

I added lru caching to the `scale` function which is called repeatedly to scale the size of the smoke particles.

This achieved a speed up of about 30% allowing frame rates of ~170 fps.

See my comments in `smoke.py` for further details.