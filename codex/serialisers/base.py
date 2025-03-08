from rest_framework import serializers


class MoonseaCodexSerialiser(serializers.ModelSerializer):
    """generic base serialise that identifies if the object can be editted"""

    editable = serializers.SerializerMethodField()

    def get_editable(self, obj):
        try:
            user = self.context.get("user")
            if not user:
                return False

            if hasattr(obj, "owner") and obj.owner == user:
                return True

            if hasattr(obj, "character") and obj.character.player == user:
                return True

            return False
        except Exception:
            return False
