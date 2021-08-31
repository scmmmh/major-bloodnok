<script lang="ts">
	import { useNavigate } from "svelte-navigator";

    const navigate = useNavigate();
    export let href: string;

    function clickHandler(ev: MouseEvent) {
        ev.preventDefault();
        if (ev.target) {
            navigate((ev.target as HTMLElement).getAttribute('href'));
        }
    }
</script>

<li>
    <a href={href} on:click={clickHandler}><slot></slot></a>
</li>
