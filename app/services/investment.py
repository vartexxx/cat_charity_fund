from app.models.base import BaseProjectModel


def invest(
        target: BaseProjectModel,
        sources: list[BaseProjectModel]
) -> list[BaseProjectModel]:
    if target.invested_amount is None:
        target.invested_amount = 0
    results = []
    for item in sources:
        transaction = min(item.remaining_amount, target.remaining_amount)
        if transaction == 0:
            break
        for obj in item, target:
            obj.invested_amount += transaction
            if obj.invested_amount == obj.full_amount:
                obj.set_fully_invested()
        results.append(item)
    return results
