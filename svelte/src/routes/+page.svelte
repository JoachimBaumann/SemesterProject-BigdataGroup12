<script>
	import { source } from 'sveltekit-sse';

	const connection = source('/api/stats_stream');
	const distance_traveled = connection.select('distance-traveled');
	const trips_completed_value = connection.select('trips-completed-value');
	const trips_completed_desc = connection.select('trips-completed-desc');
	const average_tip_value = connection.select('average-tip-value');
	const average_tip_desc = connection.select('average-tip-desc');
</script>

<div class="flex flex-col mt-4 justify-center content-center">
	<div class="stats shadow-lg">
		<div class="stat">
			<div class="stat-figure text-secondary">
				<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"
					><g
						fill="none"
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						><path
							d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"
						/><circle cx="7" cy="17" r="2" /><path d="M9 17h6" /><circle cx="17" cy="17" r="2" /></g
					></svg
				>
			</div>
			<div class="stat-title">Distance traveled</div>
			<div class="stat-value countdown">
				{$distance_traveled}
			</div>
			<div class="stat-desc">Last 60 minutes</div>
		</div>

		<div class="stat">
			<div class="stat-figure text-secondary">
				<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"
					><g
						fill="none"
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						><path d="m9 11l3 3L22 4" /><path
							d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"
						/></g
					></svg
				>
			</div>
			<div class="stat-title">Trips completed</div>
			<div class="stat-value">
				{$trips_completed_value}
			</div>
			<div class="stat-desc">
				{$trips_completed_desc}
			</div>
		</div>

		<div class="stat">
			<div class="stat-figure text-secondary">
				<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"
					><path
						fill="none"
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="m3 15l5.12-5.12A3 3 0 0 1 10.24 9H13a2 2 0 1 1 0 4h-2.5m4-.68l4.17-4.89a1.88 1.88 0 0 1 2.92 2.36l-4.2 5.94A3 3 0 0 1 14.96 17H9.83a2 2 0 0 0-1.42.59L7 19m-5-5l6 6"
					/></svg
				>
			</div>
			<div class="stat-title">Average tip</div>
			<div class="stat-value">
				{$average_tip_value}
			</div>
			<div class="stat-desc">
				{$average_tip_desc}
			</div>
		</div>
	</div>
</div>
