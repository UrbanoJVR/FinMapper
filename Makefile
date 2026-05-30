MVN := ./mvnw
APP := finmapper-desktop/target/dist/Finmapper.app

.PHONY: help clean verify package-desktop run-desktop desktop mac-app open-app

help:
	@echo "Finmapper — objetivos disponibles:"
	@echo ""
	@echo "  make clean            mvn clean en el reactor"
	@echo "  make verify           Build completo + tests de aceptación"
	@echo "  make package-desktop  ./mvnw -pl finmapper-desktop -am package"
	@echo "  make run-desktop      ./mvnw -pl finmapper-desktop javafx:run"
	@echo "  make desktop          package-desktop + run-desktop"
	@echo "  make mac-app          Genera $(APP)"
	@echo "  make open-app         open $(APP) (tras mac-app)"

clean:
	$(MVN) clean

verify:
	$(MVN) clean verify

package-desktop:
	$(MVN) -pl finmapper-desktop -am package

# Instala finmapper-app en ~/.m2 para que javafx:run resuelva el jar actual (sin -am en el reactor).
run-desktop:
	$(MVN) -pl finmapper-app install -DskipTests -q
	$(MVN) -pl finmapper-desktop javafx:run

desktop: package-desktop run-desktop

mac-app:
	$(MVN) -pl finmapper-desktop -am -Pmac-app package

open-app:
	open $(APP)
