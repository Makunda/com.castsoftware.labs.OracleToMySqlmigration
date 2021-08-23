<?xml version="1.1" encoding="UTF-8" ?>
<Package PackName="ADG_METRIC_TREE_oracleToMySqlmigration" Type="INTERNAL" Version="7.3.4.1" SupportedServer="ALL" Display="ADG Metric Tree for oracleToMySqlmigration" DatabaseKind="KB_CENTRAL" Description="">
	<Include>
	</Include>
	<Exclude>
	</Exclude>
	<Install>
    </Install>
	<Update>
    </Update>
	<Refresh>
		<Step Type="DATA" File="AdgMetrics_oracleToMySqlmigration.xml" Model="..\assessment_model_tables.xml" Scope="oracleToMySqlmigrationScope"></Step>
	</Refresh>
	<Remove>
	</Remove>
</Package>