-module(euclid).
-export([gcd/2]).

gcd(0, N) -> N;
gcd(M, N) when M < N -> gcd(N, M);
gcd(M, N) -> gcd(M rem N, N).
